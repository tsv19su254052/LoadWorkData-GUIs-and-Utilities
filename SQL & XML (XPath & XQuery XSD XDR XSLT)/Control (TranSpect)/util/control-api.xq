(:
 : functions that evaluate form fields and queries
 : and redirect to the main function with web:redirect()
 : messages and their status are returned with $msg and $msgtype
 :)
module namespace control-api            = 'http://transpect.io/control/util/control-api';
declare namespace c                     = 'http://www.w3.org/ns/xproc-step';
import module namespace svn             = 'io.transpect.basex.extensions.subversion.XSvnApi';
import module namespace control         = 'http://transpect.io/control' at '../control.xq';
import module namespace control-i18n    = 'http://transpect.io/control/util/control-i18n' at 'control-i18n.xq';
import module namespace control-util    = 'http://transpect.io/control/util/control-util' at 'control-util.xq';
import module namespace control-widgets = 'http://transpect.io/control/util/control-widgets' at 'control-widgets.xq';
(:
 : control-api:list()
 :
 : return svn:list as xml
 :)
declare
  %rest:GET
  %rest:path("/control/api/list")
  %rest:query-param("svnurl", "{$svnurl}")
  %rest:query-param("svnusername", "{$svnusername}")
  %rest:query-param("svnpassword", "{$svnpassword}")
  %output:method('xml')
function control-api:list( $svnurl as xs:string?, $svnusername as xs:string?, $svnpassword as xs:string? ) as element(c:files) {
  let $checkoutdir := control-util:get-checkout-dir($svnusername, $svnurl, $svnpassword)
  let $svninfo := svn:info($checkoutdir, $svnusername, $svnpassword)
  let $path := $svninfo/*:param[@name eq 'path']/@value
  let $revision := 'HEAD'
  let $depth := 'empty'
  let $checkout-or-update := if(file:exists($checkoutdir)) 
                             then svn:update($svnusername, $svnpassword, $checkoutdir, $revision)
                             else svn:checkout($svnurl, $svnusername, $svnpassword, $checkoutdir, $revision, $depth) 
  return svn:list( $checkoutdir, $svnusername, $svnpassword, false())
};
(:
 :  control-api:checkout()
 :    
 :  checkout a svn path according to this scheme:
 :  /workdir/username/repo/path
:)
declare
  %rest:GET
  %rest:path("/control/api/checkout")
  %rest:query-param("svnurl", "{$svnurl}")
  %rest:query-param("svnusername", "{$svnusername}")
  %rest:query-param("svnpassword", "{$svnpassword}")
  %output:method('xml')
function control-api:checkout( $svnurl as xs:string, $svnusername as xs:string, $svnpassword as xs:string ) as element(c:param-set) {
  let $checkoutdir := control-util:get-checkout-dir($svnusername, $svnurl, $svnpassword)
  let $revision := 'HEAD'
  let $depth := 'infinity'
  return svn:checkout($svnurl, $svnusername, $svnpassword, $checkoutdir, $revision, $depth)  
};
(:
 :  control-api:copy()
 :    
 :  copies a file or directory
:)
declare
  %rest:GET
  %rest:path("/control/api/copy")
  %rest:query-param("svnurl", "{$svnurl}")
  %rest:query-param("svnusername", "{$svnusername}")
  %rest:query-param("svnpassword", "{$svnpassword}")
  %rest:query-param("path", "{$path}")
  %rest:query-param("target", "{$target}")
  %output:method('xml')
function control-api:copy( $svnurl as xs:string, $svnusername as xs:string, $svnpassword as xs:string, $path as xs:string, $target as xs:string ) {
  let $commitmsg := '[control] ' || $svnusername || ': copy ' || $path || ' => ' || $target
  let $checkoutdir := control-util:get-checkout-dir($svnusername, $svnurl, $svnpassword)
  let $revision := 'HEAD'
  let $depth := 'infinity'
  let $checkout-or-update := if(file:exists($checkoutdir)) 
                             then svn:update($svnusername, $svnpassword, $checkoutdir, $revision)
                             else svn:checkout($svnurl, $svnusername, $svnpassword, $checkoutdir, $revision, $depth) 
  return svn:copy($checkoutdir, $svnusername, $svnpassword, $path, $target, ())/svn:commit($svnusername, $svnpassword, $checkoutdir, $commitmsg)
};
(:
 :  control-api:delete()
 :    
 :  delete a file or directory
:)
declare
  %rest:GET
  %rest:path("/control/api/delete")
  %rest:query-param("svnurl", "{$svnurl}")
  %rest:query-param("svnusername", "{$svnusername}")
  %rest:query-param("svnpassword", "{$svnpassword}")
  %rest:query-param("path", "{$path}")
  %output:method('xml')
function control-api:delete( $svnurl as xs:string, $svnusername as xs:string, $svnpassword as xs:string, $path as xs:string ) {
  let $force := true()
  let $commitmsg := '[control] ' || $svnusername || ': delete ' || $path
  let $checkoutdir := control-util:get-checkout-dir($svnusername, $svnurl, $svnpassword)
  let $revision := 'HEAD'
  let $depth := 'infinity'
  let $checkout-or-update := if(file:exists($checkoutdir)) 
                             then svn:update($svnusername, $svnpassword, $checkoutdir, $revision)
                             else svn:checkout($svnurl, $svnusername, $svnpassword, $checkoutdir, $revision, $depth) 
  return svn:delete($checkoutdir, $svnusername, $svnpassword, $path, $force, ())/svn:commit($svnusername, $svnpassword, $checkoutdir, $commitmsg)
};
(:
 :  control-api:move
 :    
 :  move or rename a file or directory
:)
declare
  %rest:GET
  %rest:path("/control/api/move")
  %rest:query-param("svnurl", "{$svnurl}")
  %rest:query-param("svnusername", "{$svnusername}")
  %rest:query-param("svnpassword", "{$svnpassword}")
  %rest:query-param("path", "{$path}")
  %rest:query-param("target", "{$target}")
  %output:method('xml')
function control-api:move( $svnurl as xs:string, $svnusername as xs:string, $svnpassword as xs:string, $path as xs:string, $target as xs:string ) {
  let $commitmsg := '[control] ' || $svnusername || ': move ' || $path || ' => ' || $target
  let $checkoutdir := control-util:get-checkout-dir($svnusername, $svnurl, $svnpassword)
  let $revision := 'HEAD'
  let $depth := 'infinity'
  let $checkout-or-update := if(file:exists($checkoutdir)) 
                             then svn:update($svnusername, $svnpassword, $checkoutdir, $revision)
                             else svn:checkout($svnurl, $svnusername, $svnpassword, $checkoutdir, $revision, $depth) 
  return svn:move($checkoutdir, $svnusername, $svnpassword, $path, $target, ())/svn:commit($svnusername, $svnpassword, $checkoutdir, $commitmsg)
};
(:
 :  control-api:mkdir
 :    
 :  create a directory
:)
declare
  %rest:GET
  %rest:path("/control/api/mkdir")
  %rest:query-param("svnurl", "{$svnurl}")
  %rest:query-param("svnusername", "{$svnusername}")
  %rest:query-param("svnpassword", "{$svnpassword}")
  %rest:query-param("dir", "{$dir}")
  %output:method('xml')
function control-api:mkdir( $svnurl as xs:string, $svnusername as xs:string, $svnpassword as xs:string, $dir as xs:string ) {
  let $commitmsg := '[control] ' || $svnusername || ': mkdir ' || $dir 
  let $checkoutdir := control-util:get-checkout-dir($svnusername, $svnurl, $svnpassword)
  let $path := $checkoutdir || '/' || $dir
  let $revision := 'HEAD'
  let $depth := 'infinity'
  let $checkout-or-update := if(file:exists($checkoutdir)) 
                             then svn:update($svnusername, $svnpassword, $checkoutdir, $revision)
                             else svn:checkout($svnurl, $svnusername, $svnpassword, $checkoutdir, $revision, $depth) 
  return svn:mkdir($checkoutdir, $svnusername, $svnpassword, $dir, true(), $commitmsg)/svn:commit($svnusername, $svnpassword, $path, $commitmsg)
};
(:
 :  control-api:info
 :    
 :  shows information about an object
:)
declare
  %rest:GET
  %rest:path("/control/api/info")
  %rest:query-param("svnurl", "{$svnurl}")
  %rest:query-param("svnusername", "{$svnusername}")
  %rest:query-param("svnpassword", "{$svnpassword}")
  %output:method('xml')
function control-api:info( $svnurl as xs:string, $svnusername as xs:string, $svnpassword as xs:string ) {
  svn:info($svnurl, $svnusername, $svnpassword)
};
(:
 :  control-api:propget
 :    
 :  shows information about the properties of an object
:)
declare
  %rest:GET
  %rest:path("/control/api/propget")
  %rest:query-param("svnurl", "{$svnurl}")
  %rest:query-param("svnusername", "{$svnusername}")
  %rest:query-param("svnpassword", "{$svnpassword}")
  %rest:query-param("property", "{$property}")
  %rest:query-param("revision", "{$revision}")
  %output:method('xml')
function control-api:propget( $svnurl as xs:string, $svnusername as xs:string, $svnpassword as xs:string, $property as xs:string, $revision as xs:string ) {
  svn:propget($svnurl, $svnusername, $svnpassword, $property, $revision)
};
(:
 :  control-api:propset
 :    
 :  sets properties for an object
:)
declare
  %rest:GET
  %rest:path("/control/api/propset")
  %rest:query-param("svnurl", "{$svnurl}")
  %rest:query-param("svnusername", "{$svnusername}")
  %rest:query-param("svnpassword", "{$svnpassword}")
  %rest:query-param("property", "{$property}")
  %rest:query-param("value", "{$value}")
  %output:method('xml')
function control-api:propset( $svnurl as xs:string, $svnusername as xs:string, $svnpassword as xs:string, $property as xs:string, $value as xs:string ) {
  let $commitmsg := '[control] ' || $svnusername || ': set prop: ' || $property
  let $checkoutdir := control-util:get-checkout-dir($svnusername, $svnurl, $svnpassword)
  let $svninfo := svn:info($checkoutdir, $svnusername, $svnpassword)
  let $path := $svninfo/*:param[@name eq 'path']/@value
  let $revision := 'HEAD'
  let $depth := 'empty'
  let $checkout-or-update := if(file:exists($checkoutdir)) 
                             then svn:update($svnusername, $svnpassword, $checkoutdir, $revision)
                             else svn:checkout($svnurl, $svnusername, $svnpassword, $checkoutdir, $revision, $depth)  
  return svn:propset($checkoutdir, $svnusername, $svnpassword, $property, $value)/svn:commit($svnusername, $svnpassword, $checkoutdir, $commitmsg)
};