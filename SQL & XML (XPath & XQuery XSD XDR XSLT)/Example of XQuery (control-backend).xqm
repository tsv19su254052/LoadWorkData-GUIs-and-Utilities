module namespace control-backend = 'http://transpect.io/control-backend';

import module namespace svn = 'io.transpect.basex.extensions.subversion.XSvnApi';
import module namespace control-util = 'http://transpect.io/control/util/control-util'    at '../control/util/control-util.xq';
import module namespace control = 'http://transpect.io/control' at '../control/control.xq';


(:declare
  %rest:POST("{$doc}")
  %rest:path("/control-backend/ftindex/jats")
  %rest:query-param("path-to-repo", "{$path-to-repo}", "normal")
  %rest:query-param("path-in-repo", "{$path-in-repo}", "normal")
  %updating
  %output:method("xml")
function control-backend:ftindex-jats($doc as document-node(element(*))) 
   {
    update:output(
        (<rest:response>
            <http:response status="200">
            <http:header name="Content-Language" value="en" />
            <http:header name="Access-Control-Allow-Origin" value="*" />
            <http:header name="Content-Type" value="text/xml; charset=utf-8" />
            </http:response>
        </rest:response>,
  <success/>)
  ),
    try {
      insert node $doc/* as last into db:open('CHPD_override_RDF')/*
    }
    catch * {
    }
};:)


declare
  %rest:POST("{$log}")
  %rest:path("/control-backend/{$customization}/parse-commit-log")
  %output:method("xml")
function control-backend:parse-commit-log($log as xs:string, $customization as xs:string) as element(commit) {
  let $lines as xs:string+ := tokenize($log, '[&#xa;&#xd;]+'),
      $repo-info as xs:string+ := $lines[1] => tokenize(),
      $repo-path as xs:string := $repo-info[1],
      $revision as xs:string := $repo-info[2]
  return <commit repo-path="{$repo-path}" revision="{$revision}"> {
    for $line in $lines[position() gt 1]
    let $items := $line => tokenize(),
        $action as xs:string? := switch($items[1])
                                 case 'A' return 'add'
                                 case 'U' return 'update'
                                 case '_U' return 'propupdate'
                                 case 'D' return 'delete'
                                 default return ()
    return (
      if ($action) then element{$action}{
        attribute path {$items[2]},
        if ($action eq 'propupdate')
        then control-backend:parse-prop-update(control-util:get-canonical-path($repo-path || '/' || $items[2]), $revision)
      } else ()
    )
  }</commit>
};


declare
  %rest:POST("{$log}")
  %rest:path("/control-backend/{$customization}/process-commit-log")
  %output:method("xml")
  %updating
function control-backend:process-commit-log($log as xs:string, $customization as xs:string) {
  update:output(<success/>),
  let $parsed-log := control-backend:parse-commit-log($log, $customization)
  return
    (for $pattern in ($control:config/control:ftindexes/control:file/@pattern,
                      $control:config/control:also-indexable/control:file/@pattern)
    return
      for $action in $parsed-log/*[matches(@path, $pattern)]
      return (
          switch($action/local-name())
            case 'add'
            case 'update'
              return
              for $temp-path in control-backend:get-commit-file($action/../@repo-path, $action/@path, $action/../@revision, $customization)
              return (
                control-backend:add-xml-by-path($temp-path, $action/../@repo-path || '/' || $action/@path, $customization)(:,
                file:delete(file:parent($temp-path), true()):)
              )
            case 'delete'
              return control-backend:remove-xml-by-path($action/@path, $customization)
            default return ()
      ),
      let $updated-index :=  
        copy $ind := db:open('INDEX')
        modify (
         for $action in $parsed-log/*:add
         let $svnurl := replace(control-util:get-local-path(string-join(($parsed-log/@repo-path, $action/@path), '/')), '/$', '')
         return for $target in $ind//*[@svnpath = string-join(tokenize($svnurl, '/')[not(position() = last())],'/')]
                return insert node control-util:create-path-index(control-util:get-canonical-path($svnurl), tokenize($svnurl, '/')[last()], 'directory', $target/@virtual-path || '/' || tokenize($svnurl, '/')[last()], '')
                       into $target,
         for $action in $parsed-log/*:delete
         let $svnurl := replace(control-util:get-local-path(string-join(($parsed-log/@repo-path, $action/@path), '/')), '/$', '')
         return for $target in $ind//*[@svnpath = $svnurl]
                return delete node $target,
         for $action in $parsed-log/*:propupdate
         let $svnurl := replace(control-util:get-local-path(string-join(($parsed-log/@repo-path, $action/@path), '/')), '/$', '')
         return for $target in $ind//*[@svnpath = $svnurl]
                return (for $r in $parsed-log//*:propdiff//*:removed
                        return delete node $target/*:external[@name = $r/@name],
                        for $a in $parsed-log//*:propdiff/*:added
                        let $e := for $d in $parsed-log//added
                                  return <external url="{$d/@svnurl}" mount="{$d/@name}"/>
                        return insert node control-util:create-external-path(control-util:get-canonical-path($svnurl), $e, $target/@virtual-path) into $target)
        )
        return $ind
      return control-backend:writeindextofileupdate($updated-index))
};


declare function control-backend:remove-path-index-at-svnurl($index, $svnurl as xs:string){
  let $updated-index :=  
       copy $ind := $index
       modify (
         delete node $ind//*[@svnurl eq $svnurl]
       )
       return $ind
  return $updated-index
};


declare function control-backend:parse-prop-update($svnurl as xs:string, $revision as xs:string) as element(*){
  let $pre-rev := xs:string(xs:int($revision) - 1),
      $pre := tokenize(svn:propget($svnurl,$control:svnauth,'svn:externals',$pre-rev)/*:param[@name='value']/@value,'&#xA;')[.],
      $head := tokenize(svn:propget($svnurl,$control:svnauth,'svn:externals',$revision)/*:param[@name='value']/@value,'&#xA;')[.],
      $added := $head[not(. = $pre)],
      $removed := $pre[not(. = $head)]
return 
  <propdiff>
    {for $a in $added
     let $name   := control-util:strip-whitespace(tokenize($a,' ')[last()]),
         $svnurl := control-util:get-external-url(control-util:strip-whitespace(tokenize($a,' ')[1]))
     return <added name="{$name}" svnurl="{$svnurl}"> </added>,
     for $ r in $removed
     let $name   := control-util:strip-whitespace(tokenize($r,' ')[last()]),
         $svnurl := control-util:get-external-url(control-util:strip-whitespace(tokenize($r,' ')[1]))
     return <removed name="{$name}" svnurl="{$svnurl}"> </removed>
    }
  </propdiff>
};


declare
  %updating
function control-backend:writeindextofileupdate($index) {
  file:write('basex/webapp/control/'||$control:indexfile,$index),
  db:replace('INDEX','index.xml', '/home/transpect-control/basex/webapp/control/index.xml')
};
declare function control-backend:get-commit-file($path-to-repo, $path-in-repo, $revision, $customization) as xs:string {
  (: returns the path to the file that has been saved using svnlook cat :)
  let $local-dir := '/tmp/transpect-control/commits' || $path-to-repo || '/' || replace($path-in-repo, '[^/]+$', '')
  return (
    file:create-dir($local-dir),
    proc:system(file:resolve-path('basex/webapp/control-backend/scripts/svnlook-cat.sh'), ($path-to-repo, $path-in-repo, $revision, $local-dir))
  )
};


declare
%updating
function control-backend:remove-xml-by-path($path, $customization) {
  let $dbname := string($control:config/control:db)
  return 
    for $doc in db:open($dbname, $path)
    let $lang := control-backend:determine-lang($doc)
    return (
      db:delete($control:config/control:ftindexes/control:ftindex[@lang = ($lang, 'en')[1]], $path),
      db:delete($dbname, $path)
    )
};


declare
  %rest:GET
  %rest:path("/control-backend/{$customization}/initialize")
  %updating
function control-backend:initialize($customization as xs:string) {
  update:output(<success/>),
  let $db as xs:string := string(doc('../control/config.xml')/control:config/control:db),
      $hierdir as xs:string := string(doc('../control/config.xml')/control:config/control:repos/control:repo[@role = 'hierarchy']/@path)
  return (
    for $ftdb in doc('../control/config.xml')/control:config/control:ftindexes/control:ftindex
    return
      if (db:exists(string($ftdb))) then () else
      db:create(string($ftdb), (), (), map{'language': $ftdb/@lang, 'ftindex': true(), 'diacritics': true(), 'autooptimize': true()}),
    if (db:exists(string($db))) then () else db:create($db, (), (), map{'updindex': true(), 'autooptimize': true()}),
    if (db:exists('INDEX')) then () 
        else db:create('INDEX', <root name='root' svnurl='{$hierdir}' virtual-path='{$hierdir}'/>, 'index.xml')
  )
};


declare
  %rest:GET
  %rest:path("/control-backend/{$customization}/add-xml-by-path")
  %rest:query-param("fspath", "{$fspath}")
  %rest:query-param("dbpath", "{$dbpath}", '')
  %output:method("xml")
  %updating
function control-backend:add-xml-by-path($fspath as xs:string, $dbpath as xs:string, $customization as xs:string) {
  let $doc as item() := try { doc($fspath) } 
        catch err:FODC0002 { <text/> }
        catch * { document { <error/> } },
      $lang as xs:string? := control-backend:determine-lang($doc)[. = ('de', 'en')],
      $ftdb as xs:string? := $control:config/control:ftindexes/control:ftindex[@lang = $lang] ! string(.),
      $db as xs:string := string($control:config/control:db),
      $dbpath-or-fallback := if (not($dbpath)) then $fspath else $dbpath 
  return
  (
     if ($doc/self::text) then db:replace($db, $dbpath-or-fallback, $fspath, map{'parser': 'text'})
     else (
            try {
              if ($ftdb) then db:replace($ftdb, $dbpath-or-fallback, control-backend:apply-ft-xslt($doc)) else ()
            } catch * {},
            try {
              db:replace($db, $dbpath-or-fallback, $doc)
            } catch * {
              db:replace($db, 'error/' || $dbpath-or-fallback,
              <error fspath="{$fspath}" dbpath="{$dbpath}" code="{$err:code}">
                { $err:description }
              </error>)
            }
          )
  )
};


declare
  %rest:GET
  %rest:path("/control-backend/{$customization}/add-xml-by-svn-info")
  %rest:query-param("svn-info-filename", "{$svn-info-filename}")
  %output:method("xml")
  %updating
function control-backend:add-xml-by-svn-info($svn-info-filename as xs:string, $customization as xs:string) {
  (: the fulltext and content dbs must exist before invoking this :)
  update:output(<success/>),
  let $svn-info := doc($svn-info-filename),
      $dir := file:parent($svn-info-filename)
  return
    for $entry in $svn-info/svn-info/info/entry
    let $fs-relpath := $entry/@path,
        $resolved-fs-path := file:resolve-path($fs-relpath, $dir),
        $repo-url := $entry/repository/root,
        $repo-lastpath := ($repo-url => tokenize('/'))[last()],
        $path-in-repo :=$entry/relative-url => replace('^\^', '')
    return control-backend:add-xml-by-path($resolved-fs-path, $repo-lastpath || $path-in-repo, $customization)
    (:<doc>{
      attribute fspath {$resolved-fs-path},
      attribute dbpath {$repo-lastpath || $path-in-repo}
    }</doc>:)
};


declare function control-backend:apply-ft-xslt($doc as document-node(element(*))) {
  let $ns-uri := namespace-uri-from-QName(node-name($doc/*)),
      $name := local-name($doc/*),
      $stylesheet as xs:string? := switch($ns-uri)
                                     case '' return 
                                       switch($name)
                                         case 'article'
                                         case 'book'
                                           return 'fulltext/vocabularies/bits/bits2ft.xsl'
                                         default return ()
                                     default return ()
     return if ($stylesheet) then xslt:transform($doc, $stylesheet) else $doc
};


declare function control-backend:determine-lang($doc as node()?) as xs:string? {
  ($doc/*/@xml:lang => tokenize('-'))[1]
};


declare
  %rest:GET
  %rest:path("/control-backend/{$customization}/fill-content-index-dbs")
  %rest:query-param("wcpath", "{$wcpath}")
  %output:method("xml")
  %updating
function control-backend:fill-content-index-dbs($customization as xs:string, $wcpath as xs:string?) {
  (: the fulltext and content dbs must exist before invoking this, as well as a populated INDEX db :)
  let $auth := control-util:parse-authorization(request:header("Authorization"))
  return
  if (control-util:is-admin($auth?username)) then
    let $index := db:open('INDEX', 'index.xml'),
        $hierarchy-repo := $control:config/control:repos/control:repo[@role = 'hierarchy'],
        $hierarchy-path := $hierarchy-repo/@path,
        $content-paths := $index//file/@virtual-path[matches(., $control:config/control:ftindexes/control:file/@pattern)]
    return
      for $cp in $content-paths
      let $wcp := replace($cp, '^' || $hierarchy-path, $wcpath),
          $dbp := $cp/../@svnpath
      return control-backend:add-xml-by-path($wcp, $dbp, $customization)
  else web:error(401, 'You are not permitted to fill the content index DBs')
};


declare
  %rest:GET
  %rest:path("/control-backend/{$customization}/set-updindex/{$new-val}")
  %updating
function control-backend:set-updindex($customization as xs:string, $new-val as xs:boolean) {
  update:output(<success/>),
  let $db as xs:string := $control:config/control:db => string()
  return db:optimize($db, true(), map{'updindex': $new-val})
};
