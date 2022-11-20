(:
 : functions that evaluate form fields and queries
 : and redirect to the main function with web:redirect()
 : messages and their status are returned with $msg and $msgtype
 :)
module namespace control-forms           = 'http://transpect.io/control/util/control-forms';
import module namespace svn             = 'io.transpect.basex.extensions.subversion.XSvnApi';
import module namespace control         = 'http://transpect.io/control' at '../control.xq';
import module namespace control-i18n    = 'http://transpect.io/control/util/control-i18n' at 'control-i18n.xq';
import module namespace control-util    = 'http://transpect.io/control/util/control-util' at 'control-util.xq';
import module namespace control-widgets = 'http://transpect.io/control/util/control-widgets' at 'control-widgets.xq';

(:
 : projects
 :)
declare
  %rest:GET
  %rest:path("/control/projects")
  %rest:query-param("svnurl", "{$svnurl}")
  %output:method('html')
function control-forms:projects( $svnurl as xs:string ) {
   <html>
    <head>
      {control-widgets:get-html-head($svnurl)}
    </head>
    <body>
      {control-widgets:get-page-header()}
      <main>
        {  }
      </main>
      {control-widgets:get-page-footer()}
    </body>
  </html>
};

(:
 : create dir
 :)
declare
  %rest:POST
  %rest:path("/control/create-dir")
  %rest:form-param("dirname", "{$dirname}")
  %rest:form-param("svnurl", "{$svnurl}")
function control-forms:create-dir( $dirname as xs:string?, $svnurl as xs:string ) {
  (: check if dir already exists :)
  if(normalize-space( $dirname ))
  then if(svn:info(concat( $svnurl, '/', $dirname ), $control:svnusername, $control:svnpassword )/local-name() ne 'errors')
       then web:redirect(concat( $control:siteurl||'?svnurl=', 
                                 $svnurl, '?msgtype=warning?msg=', 
                                 encode-for-uri(control-i18n:localize('dir-exists', $control:locale )))
                                 )
       else for $i in svn:mkdir( $svnurl, $control:svnauth, $dirname, false(), 'control: create dir')
            return if( $i/local-name() ne 'errors' )
                   then web:redirect($control:siteurl||'?svnurl=' || $svnurl )
                   else web:redirect(concat($control:siteurl||'?svnurl=', $svnurl, '?msgtype=error?msg=',
                                            encode-for-uri(control-i18n:localize('cannot-create-dir', $control:locale ))))
  else web:redirect($control:siteurl||'?svnurl=' || $svnurl || '?msg=' || encode-for-uri(control-i18n:localize('empty-value', $control:locale )) || '?msgtype=warning' )
};

declare
  %rest:path("/control/new-file")
  %rest:query-param("svnurl", "{$svnurl}")
  %output:method('html')
  %output:version('5.0')
function control-forms:new-file( $svnurl as xs:string ) {
  <html>
    <head>
      {control-widgets:get-html-head($svnurl)}
        <script src="{ $control:siteurl || '/static/lib/dropzone/dropzone.min.js'}" type="text/javascript"></script>
        <link rel="stylesheet" href="{$control:path || '/static/lib/dropzone/dropzone.min.css'}"></link>
    </head>
    <body>
      {control-widgets:get-page-header()}
      <main>
        <div class="upload-form">
          <dir class="dir-menu">
            <div class="dir-menu-left">
                {control-widgets:get-back-to-svndir-button($svnurl, $control:path || '/..' )}
              <div class="breadcrumb">
                {control-util:get-breadcrumb-links($svnurl)}
              </div>
                {control-widgets:create-dir-form( $svnurl, $control:path || '/../' )}
            </div>
          </dir>
        <form action="{$control:siteurl}/upload"
              class="dropzone"
              id="dropzone" method="post" enctype="multipart/form-data">
          <div class="fallback">
            <input name="file" type="file" multiple="multiple">Or select file</input>
            <input type="hidden" name="svnurl" value="{$svnurl}"/>
          </div>
        </form> 
        </div>
      </main>
      {control-widgets:get-page-footer()}
      <!-- <script src="{$control:path || '/../static/js/control.js'}" type="text/javascript"> </script> -->
        <script>
          Dropzone.options.dropzone = 
            {{ maxFilesize: {xs:string($control:max-upload-size)}, 
               dictDefaultMessage:"{control-i18n:localize('drop-files', $control:locale )}",
               params:{{svnurl:"{$svnurl}"}}
            }};
      </script>
    </body>
  </html>
};
