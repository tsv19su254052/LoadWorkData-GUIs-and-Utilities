(:
 : functions that evaluate form fields and queries
 : and redirect to the main function with web:redirect()
 : messages and their status are returned with $msg and $msgtype
 :)
module namespace control-search         = 'http://transpect.io/control/util/control-search';
import module namespace svn             = 'io.transpect.basex.extensions.subversion.XSvnApi';
import module namespace control         = 'http://transpect.io/control' at '../control.xq';
import module namespace control-i18n    = 'http://transpect.io/control/util/control-i18n' at 'control-i18n.xq';
import module namespace control-util    = 'http://transpect.io/control/util/control-util' at 'control-util.xq';
import module namespace control-widgets = 'http://transpect.io/control/util/control-widgets' at 'control-widgets.xq';

declare namespace css                   = 'http://www.w3.org/1996/css';

declare 
%rest:path('/control/cssa-rule-search-raw')
%rest:query-param("name-regex", "{$name-regex}")
%rest:query-param("occurrences", "{$occurrences}", "false")
%rest:query-param("svn-path-constraint", "{$svn-path-constraint}")
%output:method('xml')
function control-search:css-rule-search-raw($name-regex as xs:string, $occurrences as xs:boolean,
                                            $svn-path-constraint as xs:string?) {
  let $base-virtual-path := control-util:get-local-path($control:svnurlhierarchy),
      $virtual-constraint as xs:string? := $svn-path-constraint => control-util:get-virtual-path(),
      $db := db:open($control:config/control:db),
      $results 
         := for $result in $db//css:rule[matches(@native-name, $name-regex, 'i')]
            let $path := '/' || $result/db:path(.),
                $virtual-path := $path => control-util:get-virtual-path()
            where if ($svn-path-constraint) then starts-with($virtual-path, $virtual-constraint) else true()
            return <result> {
              substring-after($virtual-path, $base-virtual-path) ! (
                attribute virtual-path { . },
                attribute virtual-steps { count(tokenize(., '/')[normalize-space()]) }
              ),
              attribute dbpath { $path },
              attribute svnurl { control-util:get-canonical-path($path) },
              $result,
              if ($occurrences = true()) then 
                let $root := root($result),
                    $att-names := ($root/*/@css:rule-selection-attribute => tokenize()) 
                return for $att-name in $att-names 
                       return <xpath>{ $root//@*[name() = $att-name][. = $result/@name]/../path() }</xpath>
            } </result>
    return
    <search-results css-rule-regex="{$name-regex}" count="{count($results)}" 
      path-constraint="{$svn-path-constraint}" virtual-constraint="{$virtual-constraint}">{
      $results
    }</search-results>
};

declare 
%rest:path('/control/ftsearch-raw')
%rest:query-param("term", "{$term}")
%rest:query-param("lang", "{$lang}")
%rest:query-param("xpath", "{$xpath}")
%rest:query-param("details", "{$details}", 'true')
%rest:query-param("svn-path-constraint", "{$svn-path-constraint}")
%output:method('xml')
function control-search:ftsearch-raw($term as xs:string, $lang as xs:string*, $xpath as xs:string?, 
                                      $svn-path-constraint as xs:string?, $details as xs:boolean) {
  let $base-virtual-path := control-util:get-local-path($control:svnurlhierarchy),
      $virtual-constraint as xs:string? := $svn-path-constraint => control-util:get-virtual-path(),
      $ftdbs := $control:config/control:ftindexes/control:ftindex[@lang = $lang ! normalize-space(.)],
      $db := db:open($control:config/control:db),
      $normalized-term := ft:normalize($term),
      $normalized-xpath := if ($normalized-term) then $xpath => normalize-space() => replace('^/+', '')
                           else $xpath => normalize-space(),
      (: absolute paths – this should not be combined with full-text search as it is highly inefficient :)
      $xpath-results := if (starts-with($normalized-xpath, '/')) then 
                        for $xpath-result in xquery:eval($normalized-xpath, map { '': $db } )
                        let $path := '/' || $xpath-result/db:path(.),
                            $virtual-path := $path => control-util:get-virtual-path()
                        where if ($svn-path-constraint) 
                          then if ($virtual-constraint) 
                               then starts-with($virtual-path, $virtual-constraint) 
                               else false() (: the constraint could not be resolved to a path in the virtual hierarchy :)
                          else true()
                       return $xpath-result
                       else (),
      $xpath-results-xpaths := $xpath-results ! path(.) ! control-util:clark-to-prefix(., $control-util:namespace-map),
      $results 
         := for $ftdb in $ftdbs
            return
              for $result score $score in ft:search(string($ftdb), $term, map{'wildcards':'true', 'mode':'all words'})
              let $path := '/' || $result/db:path(.),
                  $result-xpath as xs:string? := string($result/../@path)[normalize-space()],
                  $breadcrumbs := ( ($result/ancestor::doc/*[1]/self::title, <title>[title missing]</title>)[1], 
                                    $result/ancestor::div/*[1]/self::title ),
                  $virtual-path := $path => control-util:get-virtual-path()
              where (if ($svn-path-constraint) then starts-with($virtual-path, $virtual-constraint) else true())
                    and
                      (: this is the inefficient part that will be avoided because leading slashes
                         will be stripped away if there is a full text query :)
                      (if (starts-with($normalized-xpath, '/')) 
                       then some $xpx in $xpath-results-xpaths satisfies contains($result-xpath, $xpx)
                       else if (matches($normalized-xpath, '^(\i|\.|\*)')) (: this is highly efficient :)
                            then let $modified-xpath := if (matches(tokenize($normalized-xpath, '/')[1], '^[a-z-]+::'))
                                                        then $normalized-xpath
                                                        else if (starts-with($normalized-xpath, '.'))
                                                             then $normalized-xpath
                                                             else 'ancestor-or-self::' || $normalized-xpath,
                                     $corresponding-doc as document-node(element(*)) := db:open($control:config/control:db, $result/db:path(.))[last()], 
                                     $corresponding-elt as element(*)? := if (empty($result-xpath)) then ()
                                                                          else xquery:eval($result-xpath, map { '': $corresponding-doc})
                                 return if (empty($result-xpath)) then true()
                                        else exists(xquery:eval($modified-xpath, map { '': $corresponding-elt } ))
                            else true() )
              return <result> {
                $result/../@id,
                $result/../@path,
                if (empty($result-xpath)) then attribute path {},
                substring-after($virtual-path, $base-virtual-path) ! (
                  attribute virtual-path { . },
                  attribute virtual-steps { count(tokenize(., '/')[normalize-space()]) }
                ),
                attribute dbpath { $path },
                attribute svnurl { control-util:get-canonical-path($path) },
                attribute lang { $ftdb/@lang },
                attribute ftdb { string($ftdb) },
                attribute score { $score },
                attribute breadcrumbs-signature { string-join($breadcrumbs ! generate-id(.), '_') },
                element breadcrumbs {
                  $breadcrumbs
                },
                if ($details) then
                element context {
                  ft:extract($result[. contains text {$normalized-term} using wildcards])
                }
                else ()
              } </result>
    return
    <search-results term="{$normalized-term}" xpath="{$normalized-xpath}"
      count="{if (exists($results)) then count($results) else count($xpath-results)}" 
      path-constraint="{$svn-path-constraint}" virtual-constraint="{$virtual-constraint}">{
      if (exists($results)) then $results else 
      for $xr in $xpath-results
      let $path := '/' || $xr/db:path(.),
          $virtual-path := $path => control-util:get-virtual-path()
      return <result> {
        attribute path { $xr => path() => control-util:clark-to-prefix($control-util:namespace-map) },
        substring-after($virtual-path, $base-virtual-path) ! (
          attribute virtual-path { . },
          attribute virtual-steps { count(tokenize(., '/')[normalize-space()]) }
        ),
        attribute dbpath { $path },
        attribute svnurl { control-util:get-canonical-path($path) }
      } </result>
    }</search-results>
};

declare 
%rest:path('/control/ftsearch')
%rest:query-param("term", "{$term}")
%rest:query-param("lang", "{$lang}")
%rest:query-param("xpath", "{$xpath}")
%rest:query-param("svnurl", "{$svnurl}")
%rest:query-param("restrict_path", "{$restrict_path}", 'false')
%rest:query-param("details", "{$details}", 'true')
%output:method('html')
%output:version('5.0')
function control-search:ftsearch($svnurl as xs:string?, $term as xs:string, $lang as xs:string*, $xpath as xs:string?, 
                                 $restrict_path as xs:boolean, $details as xs:boolean) {
  let $auth := control-util:parse-authorization(request:header("Authorization")),
      $used-svnurl := control-util:get-canonical-path(control-util:get-current-svnurl($auth?username, $svnurl)),
      $search-widget-function as function(xs:string?, xs:string, map(xs:string, xs:string), map(*)?, map(xs:string, item()*)? ) as item()* 
        := (control-util:function-lookup('search-form-widget'), control-widgets:search-input#5)[1],
      $rendered-result := control-search:ftsearch-raw($term, $lang, $xpath, control-util:get-local-path($svnurl)[$restrict_path = true()],
                                                      $details) 
                          => xslt:transform(doc($control:config/control:renderers/control:renderer[@role = 'fulltext-results']/@xslt), 
                                            map{'svnbaseurl': $control:svnurlhierarchy,
                                                'siteurl': $control:siteurl,
                                                'langs': string-join($lang ! normalize-space(.), ','),
                                                'term': $term,
                                                'xpath': $xpath})
  return  
  <html>
    <head>
      {control-widgets:get-html-head($used-svnurl)}
    </head>
    <body>
      {control-widgets:get-page-header( )}
      <main class="search">{
         $search-widget-function( $used-svnurl, $control:path, $auth, 
                                  map:merge(request:parameter-names() ! map:entry(., request:parameter(.))),
                                  map{'ftxp': $rendered-result}),  
        <div class="xmlsrc-container"><iframe name="xmlsrc" srcdoc="&lt;body style='font-family:sans-serif; height:100%; background-color: #eee'>&lt;p>Click on an XPath segment in the results in order to display the content here.&lt;/p>&lt;/body>"/></div>
      }</main>
      {control-widgets:get-page-footer(),
       control-widgets:create-infobox()}
    </body>
  </html>
};

declare 
%rest:path('/control/overrides-search-raw')
%rest:query-param("overrides-term", "{$overrides-term}")
%rest:query-param("type", "{$type}")
%rest:query-param("svn-path-constraint", "{$svn-path-constraint}")
%output:method('xml')
function control-search:overrides-search-raw($overrides-term as xs:string?, $type as xs:string*, 
                                            $svn-path-constraint as xs:string?) {
  let $base-virtual-path := control-util:get-local-path($control:svnurlhierarchy),
      $virtual-constraint as xs:string? := $svn-path-constraint => control-util:get-virtual-path(),
      $normalized-term := normalize-space($overrides-term),
      $results := for $path-regex in $control:config/control:also-indexable/control:file[@type = $type]/@pattern
                  let $files := db:open('INDEX', 'index.xml')//file[matches(@svnpath, $path-regex)]
                  return for $file in $files
                        where (if ($svn-path-constraint) 
                               then normalize-space($virtual-constraint)
                                    and
                                    starts-with($file/@virtual-path, $virtual-constraint) 
                               else true())
                              and
                              (if ($normalized-term) then let $doc := db:open($control:db, $file/@svnpath)
                                               return exists($doc/descendant::*/(text() , @* , comment() , 
                                                                                 processing-instruction() , 
                                                                                 processing-instruction()/name() ,
                                                                                 @*/name() ,
                                                                                 self::*[empty((self::line/parent::text| self::text)[empty(..)])]/name())
                                                                [contains(normalize-space(.), $normalized-term)])
                                          else true())
                         return
                         copy $typed-file := $file 
                           modify (
                             insert node attribute type { $path-regex/../@type } into $typed-file
                           )
                        return $typed-file
  return
  <search-results overrides-term="{$normalized-term}" 
    count="{if (exists($results)) then count($results) else 0}" 
    path-constraint="{$svn-path-constraint}" virtual-constraint="{$virtual-constraint}">{
    for $result in $results
    return <result>{
      attribute path {},
      attribute type { $result/@type },
      substring-after($result/@virtual-path, $base-virtual-path) ! (
        attribute virtual-path { . },
        attribute virtual-steps { count(tokenize(., '/')[normalize-space()]) }
      ),
      attribute dbpath { $result/@svnpath },
      attribute svnurl { control-util:get-canonical-path($result/@svnpath) }
    }</result>
  }</search-results>
};

declare 
%rest:path('/control/overrides-search')
%rest:query-param("overrides-term", "{$overrides-term}", "")
%rest:query-param("type", "{$type}")
%rest:query-param("svnurl", "{$svnurl}")
%rest:query-param("restrict_path", "{$restrict_path}", 'false')
%output:method('html')
%output:version('5.0')
function control-search:overrides-search($svnurl as xs:string?, $overrides-term as xs:string?, $type as xs:string*, 
                                        $restrict_path as xs:boolean) {
  let $auth := control-util:parse-authorization(request:header("Authorization")),
      $used-svnurl := control-util:get-canonical-path(control-util:get-current-svnurl($auth?username, $svnurl)),
      $search-widget-function as function(xs:string?, xs:string, map(xs:string, xs:string), map(*)?, map(xs:string, item()*)? ) as item()* 
        := (control-util:function-lookup('search-form-widget'), control-widgets:search-input#5)[1],
      $rendered-results := control-search:overrides-search-raw($overrides-term, $type, control-util:get-local-path($svnurl)[$restrict_path = true()]) 
                            => xslt:transform(doc($control:config/control:renderers/control:renderer[@role = 'override-results']/@xslt), 
                                              map{'svnbaseurl': $control:svnurlhierarchy,
                                                  'siteurl': $control:siteurl,
                                                  'types': string-join($type ! normalize-space(.), ','),
                                                  'overrides-term': $overrides-term})
  return  
  <html>
    <head>
      {control-widgets:get-html-head($used-svnurl)}
    </head>
    <body>
      {control-widgets:get-page-header( )}
      <main class="search">{
         $search-widget-function( $used-svnurl, $control:path, $auth, 
                                  map:merge(request:parameter-names() ! map:entry(., request:parameter(.))),
                                  map{'overrides': $rendered-results } ),  
        <div class="xmlsrc-container"><iframe name="xmlsrc" srcdoc="&lt;body style='font-family:sans-serif; height:100%; background-color: #eee'>&lt;p>Click on an XPath segment or a bullet item file name in the results in order to display the content here.&lt;/p>&lt;/body>"/></div>
      }</main>
      {control-widgets:get-page-footer(),
       control-widgets:create-infobox()}
    </body>
  </html>
};

declare 
%rest:path('/control/cssa-search-raw')
%rest:query-param("cssa-term", "{$cssa-term}")
%rest:query-param("style-type", "{$style-type}")
%rest:query-param("svn-path-constraint", "{$svn-path-constraint}")
%output:method('xml')
function control-search:cssa-search-raw($cssa-term as xs:string?, $style-type as xs:string*, 
                                        $svn-path-constraint as xs:string?) {
  let $base-virtual-path := control-util:get-local-path($control:svnurlhierarchy),
      $virtual-constraint as xs:string? := $svn-path-constraint => control-util:get-virtual-path(),
      $tokenized-term := $cssa-term => replace('˜', '~') => tokenize(),
      $results := for $rule in db:open($control:db)//css:rule
                  let $path := '/' || $rule/db:path(.),
                      $virtual-path := $path => control-util:get-virtual-path()
                  where $rule/@layout-type = $style-type
                        and
                        (if ($svn-path-constraint) 
                         then normalize-space($virtual-constraint)
                              and
                              starts-with($virtual-path, $virtual-constraint) 
                         else true())
                        and
                        (if (exists($tokenized-term))
                         then exists($rule/(@name, @native-name)[every $tt in $tokenized-term
                                                                 satisfies matches(., $tt, 'i')])
                         else true())
                  return $rule
  return
  <search-results term="{$cssa-term}" 
    count="{count($results)}" cssa-term="{string-join($tokenized-term, ',')}"
    path-constraint="{$svn-path-constraint}" virtual-constraint="{$virtual-constraint}">{
    for $result in $results
    let $path := '/' || $result/db:path(.),
        $virtual-path := $path => control-util:get-virtual-path()
    return <result>{
      attribute path { $result/path(.) => control-util:clark-to-prefix($control-util:namespace-map) },
      $result/@native-name,
      attribute style-type { $result/@layout-type },
      substring-after($virtual-path, $base-virtual-path) ! (
        attribute virtual-path { . },
        attribute virtual-steps { count(tokenize(., '/')[normalize-space()]) }
      ),
      attribute dbpath { $result/db:path(.) },
      attribute svnurl { control-util:get-canonical-path($result/db:path(.)) }
    }</result>
  }</search-results>
};

declare 
%rest:path('/control/cssa-search')
%rest:query-param("cssa-term", "{$cssa-term}", "")
%rest:query-param("style-type", "{$style-type}")
%rest:query-param("svnurl", "{$svnurl}")
%rest:query-param("restrict_path", "{$restrict_path}", 'false')
%rest:query-param("group", "{$group}", 'content-hierarchy')
%output:method('html')
%output:version('5.0')
function control-search:cssa-search($svnurl as xs:string?, $cssa-term as xs:string?, $style-type as xs:string*, 
                                    $restrict_path as xs:boolean, $group as xs:string) {
  let $auth := control-util:parse-authorization(request:header("Authorization")),
      $used-svnurl := control-util:get-canonical-path(control-util:get-current-svnurl($auth?username, $svnurl)),
      $search-widget-function as function(xs:string?, xs:string, map(xs:string, xs:string), map(*)?, map(xs:string, item()*)? ) as item()* 
        := (control-util:function-lookup('search-form-widget'), control-widgets:search-input#5)[1],
      $rendered-results := control-search:cssa-search-raw($cssa-term, $style-type, control-util:get-local-path($svnurl)[$restrict_path = true()]) 
                            => xslt:transform(doc($control:config/control:renderers/control:renderer[@role = 'cssa-results']/@xslt), 
                                              map{'svnbaseurl': $control:svnurlhierarchy,
                                                  'siteurl': $control:siteurl,
                                                  'style-types': string-join($style-type ! normalize-space(.), ','),
                                                  'group': $group,
                                                  'cssa-term': $cssa-term})
  return  
  <html>
    <head>
      {control-widgets:get-html-head($used-svnurl)}
    </head>
    <body>
      {control-widgets:get-page-header( )}
      <main class="search">{
         $search-widget-function( $used-svnurl, $control:path, $auth, 
                                  map:merge(request:parameter-names() ! map:entry(., request:parameter(.))),
                                  map{'cssa': $rendered-results } ),  
        <div class="xmlsrc-container"><iframe name="xmlsrc" srcdoc="&lt;body style='font-family:sans-serif; height:100%; background-color: #eee'>&lt;p>Click on an XPath segment or a bullet item file name in the results in order to display the content here.&lt;/p>&lt;/body>"/></div>
      }</main>
      {control-widgets:get-page-footer(),
       control-widgets:create-infobox()}
    </body>
  </html>
};



declare 
%rest:path('/control/{$customization}/render-xml-source')
%rest:query-param("svn-url", "{$svn-url}")
%rest:query-param("xpath", "{$xpath}")
%rest:query-param("highlight-xpath", "{$highlight-xpath}")
%rest:query-param("indent", "{$indent}", 'true')
%rest:query-param("text", "{$text}", 'false')
%rest:query-param("scaffold", "{$scaffold}", 'true')
%output:method('xhtml')
%output:indent('no')
function control-search:render-xml-source($svn-url as xs:string, $xpath as xs:string, $highlight-xpath as xs:string?, 
                                          $indent as xs:boolean, $scaffold as xs:boolean, $text as xs:boolean, 
                                          $customization as xs:string) {
  let $doc := db:open($control:config/control:db => string(), control-util:get-local-path($svn-url)), 
      $snippet := xquery:eval(control-util:namespace-map-to-declarations($control-util:namespace-map) || $xpath, map { '': $doc })[1],
      $reparsed as document-node(element(*)) 
        := if ($indent) then $snippet => serialize(map {'indent': true()}) => parse-xml()
           else $snippet,
      $xslt-loc as xs:string := $control:config/control:renderers/control:renderer[@role = 'raw-xml']/@xslt => string(),
      $xslt as document-node(element(*)) := doc($xslt-loc),
      $output as document-node(element(*)) 
         := $snippet => xslt:transform($xslt,
                                       map{'xpath': $xpath,
                                           'indent': $indent,
                                           'text': $text,
                                           'scaffold': $scaffold,
                                           'css-url': $control:siteurl || '/static/style.css'})
      return $output
};
