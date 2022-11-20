module namespace control-util        = 'http://transpect.io/control/util/control-util';
import module namespace svn          = 'io.transpect.basex.extensions.subversion.XSvnApi';
import module namespace control      = 'http://transpect.io/control' at '../control.xq';
import module namespace control-i18n = 'http://transpect.io/control/util/control-i18n' at 'control-i18n.xq';

declare namespace control-widgets = 'http://transpect.io/control/util/control-widgets';
declare namespace control-custom = 'http://transpect.io/control/control-customization';
declare namespace c = 'http://www.w3.org/ns/xproc-step';

declare variable $control-util:namespace-map as map(xs:string, xs:string) 
  := map {'': '',
          'css': 'http://www.w3.org/1996/css',
          'db': 'http://docbook.org/ns/docbook',
          'xhtml': 'http://www.w3.org/1999/xhtml',
          'hub': 'http://transpect.io/hub',
          'tei': 'http://www.tei-c.org/ns/1.0',
          'xlink': 'http://www.w3.org/1999/xlink'
         };

declare function control-util:namespace-map-to-declarations($map as map(xs:string, xs:string)) as xs:string {
  string-join(
    map:keys($map)[normalize-space()] ! ('declare namespace ' || . || '="' || $map(.) || '"; ')
  )
};

declare function control-util:clark-to-prefix($xpath as xs:string, $nsmap as map(xs:string, xs:string)) as xs:string {
  fold-left(
    map:keys($nsmap), 
    $xpath, 
    function($xp, $prefix) { 
      $xp => replace('/Q\{' || $nsmap($prefix) || '\}', '/' || $prefix || ':'[normalize-space($prefix)]) 
    }
  )
};


(: 
 : prints the parent directory of a path,
 : e.g. /home/parentdir/mydir/ => /home/parentdir/ 
 :)  
declare function control-util:path-parent-dir( $path as xs:string ) as xs:string? {
  let $local-path := control-util:get-local-path($path),
      $parent-path := ($control:index//*[@svnpath eq $local-path]
            /parent::*/@svnpath)[1]
  return if ($parent-path)
         then control-util:get-canonical-path($parent-path)
         else ''
};

(:
 : decode escaped characters within an URI 
 :)
declare function control-util:decode-uri( $uri as xs:string ) {
  for $i in analyze-string($uri, '%\d{2}')/*
  return string-join(if($i/self::fn:match )
                     then codepoints-to-string(convert:integer-from-base(replace($i, '%(\d{2})', '$1'), 16))
                     else $i, 
                     '')
};

(:
 : get icon url for an icon name
 :)
declare function control-util:get-mimetype-url( $ext as xs:string? ) as xs:string {
  if (( $ext ) eq 'folder')
  then 'static/icons/flat-remix/Flat-Remix-Blue-Dark/places/scalable/folder-black.svg'
    else if ($ext = 'external')
    then 'static/icons/flat-remix/Flat-Remix-Blue-Dark/places/scalable/folder-black-documents.svg'
    else 'static/icons/flat-remix/Flat-Remix-Blue-Dark/mimetypes/scalable/' || control-util:ext-to-mimetype( $ext ) || '.svg' 
};

(:
 : check if svnurl is a local repo
 :)
declare function control-util:is-svn-repo( $svnurl as xs:string ) as xs:boolean {
  let $children := svn:list($svnurl, $control:svnusername, $control:svnpassword, false())//*:directory
  return count($children[@name = ("locks", "hooks", "db")]) ge 3
};

(:
 : check if svnurl is a local repo with external url
 :)
declare function control-util:is-local-repo( $svnurl as xs:string ) as xs:boolean {
  false()};

declare
function control-util:writeindextofile($index) {
  file:write('basex/webapp/control/'||$control:indexfile,$index)
};

declare function control-util:create-path-index($svnurl as xs:string,
                                                $name as xs:string?,
                                                $type as xs:string, 
                                                $virtual-path as xs:string,
                                                $mount-point as xs:string?){
  if (svn:list($svnurl, $control:svnauth, false())[not(*:error)])
  then 
    element {$type} {
(:      attribute raw {$svnurl || '--' || $name || '--' || $type || '--' || $virtual-path || '--' ||$mount-point}, :)
      attribute name {$name},
      if ($type = 'directory') then prof:dump(string-join((convert:integer-to-dateTime(prof:current-ms()), $svnurl, control-util:get-local-path($svnurl)), ' ')) else (),
      attribute svnpath {control-util:get-local-path($svnurl)},
      attribute virtual-path {control-util:get-local-path($virtual-path)},
      for $d in svn:list($svnurl,$control:svnauth, false())/*[not(self::*:error)]
      let $sub := control-util:create-path-index(concat($svnurl,'/',$d/@name),
                                                 $d/@name,
                                                 $d/local-name(), 
                                                 $virtual-path || '/' || $d/@name,
                                                 $mount-point)
      return $sub,
      for $e in control-util:parse-externals-property(svn:propget($svnurl, $control:svnauth, 'svn:externals', 'HEAD'))
      return 
        control-util:create-external-path($svnurl, $e, $virtual-path)
    }
};

declare function control-util:create-external-path($svnurl as xs:string, $external, $virtual-path as xs:string) {
  <external name="{$external/@mount}" 
            svnpath="{control-util:get-local-path($external/@url)}" 
            mount-point="{control-util:get-local-path($svnurl || '/' || $external/@mount)}" 
            virtual-path="{control-util:get-local-path($virtual-path) || '/' || $external/@mount}">
    {for $f in svn:list(xs:string($external/@url),$control:svnauth, false())/*
     let $subf := control-util:create-path-index(string-join((xs:string($external/@url),$f/@name),'/'),
                                                 $f/@name,
                                                 $f/local-name(),
                                                 $virtual-path || '/' || $external/@mount ||  '/' || $f/@name,
                                                 $svnurl || '/' || $external/@mount)
     return $subf}
  </external>
};

declare function control-util:get-svnurl-parent-from-index($svnurl as xs:string) {
  db:open('INDEX')//*[@svnurl eq $svnurl]/parent::*/@svnurl
};

declare function control-util:get-permissions-for-file($svnurl as xs:string,
                                                       $file as xs:string,
                                                       $access){
  let $selected-repo := tokenize(svn:info($svnurl, $control:svnauth)/*:param[@name = 'root-url']/@value,'/')[last()],
      $selected-filepath := replace(replace(replace(string-join(($svnurl,$file),'/'),'/$',''),svn:info($svnurl, $control:svnauth)/*:param[@name = 'root-url']/@value,''),'^/',''),
      $admin-group := $access//control:groups/control:group[control:name = 'admin'],
      $explicit-permissions := for $group in $access//control:groups/control:group except $admin-group
                               let $p := $access//control:rels/control:rel[control:file = $selected-filepath]
                                                                          [control:repo = $selected-repo]
                                                                          [control:permission]
                                                                          [control:group = $group/control:name]
                               return if ($p) 
                                      then element permission { element g {$group/control:name/text()},
                                                                element p {$p/control:permission/text()},
                                                                element i {false()}},
      $implicit-permissions := for $group in $access//control:groups/control:group except $admin-group
                               let $writeable-repos := $access//control:rels/control:rel[control:group = $group]
                                                                                        [control:repo]
                                                                                        [not(control:file)],
                                   $p := if (control-util:or(for $r in $writeable-repos return matches($selected-repo,$r/control:repo)))
                                         then 'write'
                                         else 'read'
                               return element permission { element g {$group/control:name/text()},
                                                           element p {$p},
                                                           element i {true()}}
  return for $group in $access//control:groups/control:group
         return ($explicit-permissions[g = $group/control:name], $implicit-permissions[g = $group/control:name])[1]
         
};

declare function control-util:or($bools as xs:boolean*) as xs:boolean{
  count($bools[. = true()]) > 0
};

declare function control-util:is-file($file as xs:string?) as xs:boolean{
  matches($file,'\.')
};

declare function control-util:short-size($size as xs:integer) as xs:string {
  let $B := $size,
      $KB := $size div 1024,
      $MB := $KB div 1024,
      $GB := $MB div 1024
  return      if ( $KB lt 1024) then format-number($KB,'#,##0.00') ||'&#x202f;KB'
         else if ( $MB lt 1024) then format-number($MB,'#,###.00') ||'&#x202f;MB'
                           else format-number($GB,'#,###.00') ||'&#x202f;GB'
        
};

declare function control-util:get-breadcrumb-links($svnurl as xs:string){
  let $virtual-position := $control:index//*[@svnpath = control-util:get-local-path($svnurl)],
      $parents := $virtual-position/ancestor-or-self::*,
      $links := for $p in $parents/@svnpath
         return <a href="{$control:siteurl|| '?svnurl=' || $p}">{tokenize($p,'/')[last()]}</a>
  return for $l in $links
         return ($l,'/')
};

declare function control-util:split-string-at-length($str as xs:string?, $length as xs:integer) as xs:string* {
  for $i in (1 to (xs:integer(ceiling(string-length($str) div $length))))
  return substring($str, ($i - 1) * $length + 1, $length)
};

declare function control-util:svnurl-to-link($svnurl as xs:string?) as element(a){
  <a href="{$control:siteurl || '?svnurl=' || $svnurl}">{$svnurl}</a>
};

declare function control-util:virtual-path-to-svnurl($virtual-path as xs:string) as xs:string{
  let $svnpath := $control:index//*[@virtual-path eq control-util:get-local-path($virtual-path)]/@svnpath
  return if ($svnpath) then $svnpath else $virtual-path
};

declare function control-util:strip-whitespace($s as xs:string) as xs:string{
  let $start := replace($s,'^\p{Zs}','')
  return replace($start,'\p{Zs}$','')
};

declare function control-util:get-short-string($str as xs:string, $length as xs:integer) as xs:string {
  concat(
    control-util:split-string-at-length(xs:string($str),$length - 5)[1],
      if (string-length(xs:string($str)) gt ($length - 5))  
      then '...' 
      else '')
};

declare function control-util:update-path-index-at-svnurl($index, $svnurl as xs:string){
  let $updated-index :=  
       copy $ind := $index
       modify (
         for $t in $ind//*[@svnurl eq $svnurl]
         return replace node $t with
           control-util:create-path-index($svnurl,
                                          tokenize($svnurl,'/')[last()],
                                          $t/local-name(), 
                                          $t/@virtual-path, 
                                          $t/@mount-point)
       )
       return $ind
  return $updated-index
};

declare function control-util:pad-text($string as xs:string?, $length as xs:integer) as xs:string{
  concat($string, string-join(for $x in 1 to ($length - string-length($string)) return ' ', ""))
};

declare function control-util:create-download-link($svnurl as xs:string, $file as xs:string?) as xs:string{
  let $result := string-join((control-util:get-canonical-path($svnurl),$file),'/')
  return $result
};

declare function control-util:get-local-path($svnurl as xs:string?) as xs:string? {
  let $repo := control-util:get-repo-for-svnurl($svnurl),
      $repourl := if ($repo/@parent-path) then $repo/@parent-path else $repo/@path,
      $local-path := replace($repourl,'/$',''),
      $canon-path := replace($repo/@canon-path,'/$','')
  return if ($repo)  then replace($svnurl,'^'||$canon-path, $local-path) else $svnurl
};

declare function control-util:get-canonical-path($svnurl as xs:string) as xs:string{
  let $repo := control-util:get-repo-for-svnurl($svnurl),
      $repourl := if ($repo/@parent-path) then $repo/@parent-path else $repo/@path,
      $local-path := replace($repourl,'/$',''),
      $canon-path := replace($repo/@canon-path,'/$','')
  return if ($repo) then replace($svnurl, '^'||$local-path, $canon-path) else $svnurl
};

declare function control-util:get-repo-for-svnurl($svnurl as xs:string?) as element(control:repo)?{
  let $path-repos := $control:repos/control:repo[@path][contains($svnurl, replace(@path,'/$',''))],
      $parent-path-repos := $control:repos/control:repo[@parent-path][contains($svnurl, replace(@parent-path,'/$',''))],
      $canon-path-repos := $control:repos/control:repo[@canon-path][contains($svnurl, replace(@canon-path,'/$',''))],
      $all-repos := ($path-repos,$parent-path-repos, $canon-path-repos)
  return if (count($all-repos) gt 0) then $all-repos[1] else ()
};

declare function control-util:get-virtual-path($url-or-path as xs:string?) as xs:string? {
  control-util:get-local-path($url-or-path) !
    (db:attribute('INDEX', ., 'svnpath')/../@virtual-path,
     db:attribute('INDEX', ., 'path')/../@mount-point,
     db:attribute('INDEX', ., 'virtual-path'),
     db:attribute('INDEX', ., 'mount-point')
    )[1] => string()
};

declare function control-util:get-permission-for-group($group as xs:string, $repo as xs:string, $access) as xs:string?{
  let $writeable-repos := $access//control:rels/control:rel[control:group = $group]
                                                      [control:repo]
                                                      [not(control:file)],
      $indirect-permission := if (control-util:or(for $r in $writeable-repos return matches($repo,$r/control:repo)))
                              then 'write'
                              else 'read',
      $direct-permission := $access//control:rels/control:rel[control:group = $group]
                                                              [control:repo  =$repo]
                                                              [control:permission]
                                                              [control:file = '']/control:permission,
      $combined-permission := ($direct-permission,$indirect-permission)[1],
      $selected-permission := if ($combined-permission = 'none') then ''
                              else if ($combined-permission = 'read') then 'r'
                              else if ($combined-permission = 'write') then 'rw'
  return $selected-permission
};

declare function control-util:add-user-to-mgmt($username as xs:string, $defaultsvnurl as xs:string?){
  let $file := $control:mgmtdoc
  return if (not($file//control:users/control:user[control:name = $username]))
         then file:write("basex/webapp/control/"||$control:mgmtfile,
           if ($defaultsvnurl)
           then $file update {insert node element user {element name {$username}} into .//*:users}
                      update {insert node element rel  {element user {$username},
                                                        element defaultsvnurl {$defaultsvnurl}} into .//*:rels}
           else $file update insert node element user {element name {$username}} into .//*:users)
};

declare function control-util:get-permission-for-user($user as xs:string, $repo as xs:string, $access) as xs:string?{
  for $group in $access/control:groups/control:group/control:name
  let $rels := $access//control:rels/control:rel[control:user = $user]
                                               [control:group],
      $permission := control-util:get-permission-for-group($group, $repo, $access)
  where exists($access/control:rels/control:rel[control:user = $user][control:group = $group])
  return $permission
};

declare function control-util:get-message-url($msg as xs:string, $msgtype as xs:string, $first as xs:boolean, $localize as xs:boolean)
{
  let $message := if ($first) then '?msg=' else  '&amp;msg=',
      $messagetype := '&amp;msgtype=' || $msgtype
  return $message || encode-for-uri(if ($localize) then control-i18n:localize($msg, $control:locale) else $msg) || $messagetype
};

(:
 : get mimetype for file extension
 :)
declare function control-util:ext-to-mimetype( $ext as xs:string? ) as xs:string {
     if ( $ext eq 'xml')              then 'text-xml'
else if ( $ext eq 'text')             then 'text-plain'
else if ( $ext = ('Makefile', 'bat')) then 'text-x'
else                                      'text-plain'
};

(:
 : is user admin
 :)
declare function control-util:is-admin( $username as xs:string) as xs:boolean {
let $user := $control:access//*:users/*:user[*:name=$username],
    $grouprels := $control:access//*:rels/*:rel[*:user][*:user=$user/*:name]
 return "admin" = $grouprels/*:group
};

(:
 : get read/write for username and repo
 :)
declare function control-util:get-rights( $username as xs:string, $repotitle as xs:string? ) as xs:string {
let  $user := $control:access//*:users/*:user[*:name=$username],
 $grouprel := $control:access//*:rels/*:rel[*:user][*:user=$user/*:name],
    $group := $control:access//*:groups/*:group[*:name = $grouprel/*:group],
     $rels := $control:access//*:rels/*:rel[*:repo][*:group=$group],
    $repos := $control:access//*:repos/*:repo[matches(*:title,string-join($rels/*:repo/text(),"|"))]
 return if ((control-util:is-admin($username)) or ($repotitle = $repos/*:title))
        then "write"
        else "read"
};

declare function control-util:normalize-repo-url( $url as xs:string ) as xs:string {
  replace($url, '\p{P}', '_')
};

declare function control-util:get-defaultsvnurl-from-user($username as xs:string) as xs:string?{
  $control:access//control:rels/control:rel[control:user = $username][control:defaultsvnurl]/control:defaultsvnurl/text()
};

declare function control-util:get-current-svnurl($username as xs:string, $svnurl as xs:string?) as xs:string {
  ($svnurl,
    session:get('svnurl'),
    control-util:get-defaultsvnurl-from-user($username),
    $control:default-svnurl,
    $control:svnurlhierarchy)[. != ''][1]
};

declare function control-util:get-checkout-dir($svnusername as xs:string, $svnurl as xs:string, $svnpassword as xs:string) as xs:string {
  let $svninfo := svn:info($svnurl, $svnusername, $svnpassword)
  let $repo := control-util:normalize-repo-url($svninfo/*:param[@name eq 'root-url']/@value)
  let $path := $svninfo/*:param[@name eq 'path']/@value
  return $control:datadir || file:dir-separator() || $svnusername || file:dir-separator() || $repo || file:dir-separator() || $path
};

declare function control-util:parse-externals-property($prop as element(*)) as element(external)* {
  for $line in 
    ($prop/self::c:param-set[c:param[@name='property'][@value='svn:externals']]/c:param[@name='value']/@value
     => tokenize('[&#xa;&#xd;]+'))[normalize-space()]
  return <external> {
    let $tokens as xs:string+ := $line => tokenize('\s+'),
        $url-plus-rev := $tokens[matches(., '^https?:')],
        $mount as xs:string* := $tokens[not(matches(., '^https?:'))],
        $rev as xs:string* := ($url-plus-rev[contains(., '@')] => tokenize('@'))[last()],
        $url := replace(replace($url-plus-rev, '^(.+)(@.*)?$', '$1'),'localhost:'|| $control:port,'127.0.0.1')
    return (attribute url { $url },
            if(exists($rev)) then attribute rev { $rev } else (),
            attribute mount { $mount })
  }</external>
};

declare function control-util:parsed-external-to-string($parsed as element(externals)) as xs:string {
   string-join(for $p in $parsed//*:external return $p/@url || ' ' || $p/@mount, '&#xA;')
};

declare function control-util:get-external-url($url as xs:string) as xs:string {
    replace(replace($url, '^(.+)(@.*)?$', '$1'),'localhost:'|| $control:port,'127.0.0.1')
};

declare function control-util:post-file-to-converter($svnurl as xs:string, $file as xs:string, $convertername as xs:string, $type as xs:string) as element(conversion) {
(: $converter := hobots, $type := idml2tex:)
  let $filepath      := '/home/transpect-control/upload',
      $remove-folder := proc:execute('rm', ('-r',$filepath)),
      $prepare-file  := proc:execute('mkdir', ($filepath, '-p')),
      $checkout      := proc:execute('svn',('co', $svnurl, $filepath, '--username',$control:svnusername,'--password',$control:svnpassword)),
      $upload-call   := ('-F', 'type='||$type, '-F','input_file=@'||$filepath||'/'||$file, '-u', $control:svnusername||':'||$control:svnpassword,control-util:get-converter-function-url($convertername,'upload')),
      $upload        := proc:execute('curl',('-F', 'type='||$type, '-F','input_file=@'||$filepath||file:dir-separator()||$file, '-u', $control:svnusername||':'||$control:svnpassword,control-util:get-converter-function-url($convertername,'upload'))),
      $upload_res    := json:parse($upload/output),
      $status        := proc:execute('curl',('-u', $control:svnusername||':'||$control:svnpassword,control-util:get-converter-function-url($convertername,'status')||'?input_file='||$file||'&amp;type='||$type)),
      $status_res    := json:parse($status/output),
      $result_xml    := 
        <conversion>
          <input>{string-join(($svnurl, $file, $convertername, $type),'||')}</input>
          <id>{random:uuid()}</id>
          <type>{$upload_res/json/conversion__type/text()}</type>
          <file>{$file}</file>
          <svnurl>{$svnurl}</svnurl>
          <status>{if ($upload_res/json/status/text()) then $upload_res/json/status/text() else 'failed'}</status>
          <messages>{for $m in $status_res/json/message/* 
                     return element message {text {$m/text()}}}</messages>
          <result_files></result_files>
          <callback>{$upload_res/json/callback__uri/text()}</callback>
          <delete>{$status_res/json/delete__uri/text()}</delete>
          <result_list>{$status_res/json/result__list__uri/text()}</result_list>
        </conversion>
  return $result_xml
};

(:
 : get running conversions
 :)
declare function control-util:get-running-conversions($svnurl as xs:string, $file as xs:string, $type as xs:string) {
  let $conversions := $control:conversions//control:conversion[control:type = $type][control:file = $file][control:svnurl = $svnurl]
  return $conversions
};

(:
 : start new conversion and save it
 :)
declare function control-util:start-new-conversion($svnurl as xs:string, $file as xs:string, $type as xs:string) {
  let $conv := control-util:post-file-to-converter($svnurl, $file, control-util:get-converter-for-type($type)/@name, $type)
  return $conv
};

declare function control-util:get-converters-for-file($file as xs:string) as xs:string* {
     let $ext := replace($file,'.*\.([^\.]+)','$1')
  return $control:converters//control:type[matches(@name,concat('^',$ext))]/@type
};

declare function control-util:add-conversion($conv as element(conversion)) {
  let $file := $control:mgmtdoc, $updated-conversions := $file update {insert node $conv into //control:conversions}
  return file:write("basex/webapp/control/"||$control:mgmtfile, $updated-conversions)
};

declare function control-util:update-conversion($id as xs:string){
  let $conversion := $control:conversions//control:conversion[control:id eq $id],
      $type  := $conversion/control:type,
      $convertername := control-util:get-converter-for-type($type)/@name,
      $file       := $conversion/control:file/text(),
      $status     := proc:execute('curl',('-u', $control:svnusername||':'||$control:svnpassword,control-util:get-converter-function-url($convertername,'status')||'?input_file='||$file||'&amp;type='||$type)),
      $status_res := json:parse($status/output),
      $result_files := proc:execute('curl',('-u', $control:svnusername||':'||$control:svnpassword,$conversion/control:result_list)),
      $result_files_res := json:parse($result_files/output),
      $formatted-files := for $f in $result_files_res//*:files/* 
                          let $name := replace($f//*:download__uri/text(),'.*\?file=([^&amp;]*)(&amp;.*|$)','$1')
                          return element file {attribute name {$name},
                                               element download {$f//*:download__uri/text()}},
      $updated-conversion := 
        copy $old := $conversion
        modify (
          replace value of node $old//control:status with if ($status_res/json/status/text()) then $status_res/json/status/text() else 'failed',
          replace node $old//control:messages with element messages {
                           for $m in $status_res/json/message/* return element message {text {$m/text()}}},
          replace node $old//control:result_files with element result_files {
                           $formatted-files}
        )
        return $old,
      $file := $control:mgmtdoc,
      $updated-access := $file update {delete node //control:conversion[control:id = $id]}
                               update {insert node $updated-conversion into .//control:conversions},
      $updated-file := file:write("basex/webapp/control/"||$control:mgmtfile, $updated-access)
  return $updated-file
};

declare function control-util:get-converter-for-type($type as xs:string) as element(control:converter){
  $control:converters/control:converter[descendant::control:type[@type = $type]]
};

declare function control-util:get-current-url() as xs:string {
  replace(request:uri(),'https?://[^/]+/control',$control:siteurl)
};

declare function control-util:get-query-without-msg() as xs:string{
  let $queries-to-remove := '^msg=,^msgtype=' 
  return string-join(tokenize(request:query(),'&amp;')[not(matches(.,string-join(tokenize($queries-to-remove,","),"|")))],'&amp;')
};

declare function control-util:get-url-without-msg(){
  let $query := control-util:get-query-without-msg(),
      $url := control-util:get-current-url()
  return $url || '?' || $query
};

declare function control-util:get-converter-function-url($name as xs:string, $type as xs:string){
  let $converter := $control:converters/control:converter[@name = $name]
  return $converter/control:base/text()||$converter/control:endpoints/*[local-name(.) = $type]/text()
};

declare function control-util:writegroups($access) as xs:string {
    string-join(('[groups]',
    for $group in $access//control:groups/control:group (:groups:)
    where $access//control:rels/control:rel[control:user][control:group=$group/control:name]
    return concat($group/control:name,' = ',string-join(
      for $rel in $access//control:rels/control:rel[control:user][control:group = $group/control:name] (:user:)
      return $rel/*:user,', ')
    )),$control:nl)
};

declare function control-util:function-lookup ( $role as xs:string ) as function(*)? {
  $control:config/control:functions/control:function[@role = $role]
    ! function-lookup(xs:QName(@name), @arity)
};

declare function control-util:parse-authorization($header as xs:string?) as map(xs:string, xs:string)? {
  for $h in $header
  let $credentials := $h => substring(6)
                         => xs:base64Binary()
                         => bin:decode-string()
                         => tokenize(':')
  return map{'username':$credentials[1],'cert-path':'', 'password': $credentials[2]}
};
