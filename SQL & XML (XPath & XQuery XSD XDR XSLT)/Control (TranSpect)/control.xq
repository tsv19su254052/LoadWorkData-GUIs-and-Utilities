(:
 : transpect control 202202181307
 :)
module namespace        control         = 'http://transpect.io/control';
import module namespace session         = "http://basex.org/modules/session";
import module namespace svn             = 'io.transpect.basex.extensions.subversion.XSvnApi';
import module namespace control-actions = 'http://transpect.io/control/util/control-actions' at 'util/control-actions.xq';
import module namespace control-api     = 'http://transpect.io/control/util/control-api'     at 'util/control-api.xq';
import module namespace control-i18n    = 'http://transpect.io/control/util/control-i18n'    at 'util/control-i18n.xq';
import module namespace control-util    = 'http://transpect.io/control/util/control-util'    at 'util/control-util.xq';
import module namespace control-widgets = 'http://transpect.io/control/util/control-widgets' at 'util/control-widgets.xq';
import module namespace control-backend = 'http://transpect.io/control-backend' at '../control-backend/control-backend.xqm';

declare variable $control:config          := doc('config.xml')/control:config;
declare variable $control:locale          := $control:config/control:locale;
declare variable $control:customization as xs:string := $control:config/control:customization;
declare variable $control:host            := $control:config/control:host;
declare variable $control:port            := $control:config/control:port;
declare variable $control:path            := $control:config/control:path;
declare variable $control:datadir         := $control:config/control:datadir;
declare variable $control:db              := $control:config/control:db;
declare variable $control:max-upload-size := $control:config/control:max-upload-size;
declare variable $control:default-svnurl  := $control:config/control:defaultsvnurl;
declare variable $control:repos           := $control:config/control:repos;
declare variable $control:mgmtfile        := 'control.xml';
declare variable $control:mgmtdoc         := doc('control.xml');
declare variable $control:access          := $control:mgmtdoc//control:access;
declare variable $control:conversions     := $control:mgmtdoc//control:conversions;
declare variable $control:indexfile       := 'index.xml';
declare variable $control:index           := doc($control:indexfile)/root;
declare variable $control:svnurlhierarchy := $control:config/control:svnurlhierarchy;
declare variable $control:svnbasewerke    := $control:config/control:svnbasewerke;
declare variable $control:repobase        := "/content/hierarchy";
declare variable $control:protocol        := if ($control:port = '443') then 'https' else 'http';
declare variable $control:siteurl         := $control:protocol || '://' || $control:host || ':' || $control:port || $control:path;
declare variable $control:svnusername     := xs:string($control:config/control:svnusername);
declare variable $control:svnpassword     := xs:string($control:config/control:svnpassword);
declare variable $control:htpasswd        := $control:config/control:htpasswd;
declare variable $control:svnauth         := map{'username':$control:svnusername,'cert-path':'', 'password': $control:svnpassword};
declare variable $control:svnurl          := (request:parameter('svnurl'), xs:string(doc('config.xml')/control:config/control:svnurl))[1];
declare variable $control:msg             := request:parameter('msg');
declare variable $control:msgtype         := request:parameter('msgtype');
declare variable $control:action          := request:parameter('action');
declare variable $control:file            := request:parameter('file');
declare variable $control:dest-svnurl     := request:parameter('dest-svnurl');
declare variable $control:svnauthfile     := "/etc/svn/default.authz";
declare variable $control:htpasswd-script := "basex/webapp/control/htpasswd-wrapper.sh"; 
declare variable $control:htpasswd-group  := $control:config/control:htpasswd-group;
declare variable $control:htpasswd-file   := $control:config/control:htpasswd-file;
declare variable $control:converters      := $control:config/control:converters;
declare variable $control:default-permission
                                          := "r";
declare variable $control:nl              := "
";

declare
%rest:path('/control')
%rest:query-param("svnurl", "{$svnurl}")
%rest:form-param("svnurl", "{$form-svnurl}")
%output:method('html')
%output:version('5.0')
function control:control($svnurl as xs:string?, $form-svnurl as xs:string?) {
  let $auth := control-util:parse-authorization(request:header("Authorization")),
      $used-svnurl := ($svnurl, $form-svnurl)[1]
  return 
    if ($used-svnurl and control-util:get-canonical-path($used-svnurl) eq $used-svnurl) 
    then control:main( $used-svnurl ,$auth)
    else web:redirect($control:siteurl || '?svnurl=' || control-util:get-canonical-path(control-util:get-current-svnurl(map:get($auth,'username'), $used-svnurl)))
};


(:
 : this is where the "fun" starts...
 :)
declare function control:main( $svnurl as xs:string?, $auth as map(*)) as element(html) {
  let $used-svnurl := control-util:get-canonical-path(control-util:get-current-svnurl($auth?username, $svnurl)),
      $search-widget-function as function(xs:string?, xs:string, map(xs:string, xs:string), map(*)?, map(xs:string, item()*)? ) as item()* 
        := (control-util:function-lookup('search-form-widget'), control-widgets:search-input#5)[1],
      $known-user := control-util:add-user-to-mgmt(xs:string(map:get($auth,'username')),())
  return
  <html>
    <head>
      {control-widgets:get-html-head($used-svnurl)}
    </head>
    <body>
      {control-widgets:get-page-header( ),
       if( normalize-space($control:action) and normalize-space($control:file) )
       then control-widgets:manage-actions( $used-svnurl, ($control:dest-svnurl, $used-svnurl)[1], $control:action, $control:file )
       else ()}
      <main>{
         control:get-message( $control:msg, $control:msgtype),
         if(normalize-space( $used-svnurl ))
         then control-widgets:get-dir-list( $used-svnurl, $control:path, control-util:is-local-repo($used-svnurl), $auth)
         else 'URL parameter empty!',
         $search-widget-function( $used-svnurl, $control:path, $auth, 
                                  map:merge(request:parameter-names() ! map:entry(., request:parameter(.))),
                                  () )  
      }</main>
      {control-widgets:get-page-footer(),
       control-widgets:create-infobox()}
    </body>
  </html>
};
(:
 : Get SVN Log info for svnurl
 :)
declare
%rest:path('/control/getsvnlog')
%rest:query-param("svnurl", "{$svnurl}")
%rest:query-param("file", "{$file}")
%output:method('html')
%output:version('5.0')
function control:get-svnlog($svnurl as xs:string?, $file as xs:string?) as element() {
  let $auth := control-util:parse-authorization(request:header("Authorization")),
      $svnlog := if ($file) then svn:log( control-util:virtual-path-to-svnurl($svnurl || '/' || $file),$auth,0,0,0)
                            else svn:log( control-util:virtual-path-to-svnurl($svnurl),$auth,0,0,0),
      $monospace-width := 75
  return <pre class="monospace">
  {for $le in $svnlog/*:logEntry
                   return
                     (' Revision | Author    | Date                                         ', 
                     <br/>,
                     ' ' || control-util:pad-text($le/@revision,8) || 
                     ' | ' || control-util:pad-text($le/@author,9) || 
                     ' | ' || $le/@date, <br/>,
                     ' ' ,(for $str in control-util:split-string-at-length($le/@message,$monospace-width - 2)
                             return ('' || $str, <br/>)),
                          (for $file in $le//*:changedPath
                             return (<a href="{$control:siteurl || '?svnurl=' || $svnurl 
                                            || string-join(tokenize(xs:string($file/@name),'/')[not(matches(.,'\....+$'))],'/')}">
                                             {control-util:get-short-string(xs:string($file/@type || ' ' || $file/@name), $monospace-width)}
                                     </a>)),<br/>,
                     '--------------------------------',<br/>)
   }
  </pre>
};
(:
 : Get SVN info for svnurl
 :)
declare
%rest:path('/control/getsvninfo')
%rest:query-param("svnurl", "{$svnurl}")
%rest:query-param("file", "{$file}")
%output:method('html')
%output:version('5.0')
function control:get-svninfo($svnurl as xs:string?, $file as xs:string?) as element() {
  let $auth := control-util:parse-authorization(request:header("Authorization")),
      $svninfo := svn:info( control-util:get-canonical-path(control-util:virtual-path-to-svnurl($svnurl || '/' || $file)),$control:svnauth),
      $monospace-width := 75
  return 
  <pre class="monospace">
   {
      let $date := xs:string($svninfo/*:param[matches(@name, 'date')]/@value),
          $path := xs:string($svninfo/*:param[matches(@name, 'path')]/@value),
          $rev  := xs:string($svninfo/*:param[matches(@name, 'rev')]/@value),
          $author := xs:string($svninfo/*:param[matches(@name, 'author')]/@value),
          $root-url  := xs:string($svninfo/*:param[matches(@name, 'root-url')]/@value),
          $url  := xs:string($svninfo/*:param[matches(@name, '^url')]/@value)
      return 
        ('Path: ', $path,<br/>,
'URL: ', control-util:svnurl-to-link($url),<br/>,
'Root URL: ', control-util:svnurl-to-link($root-url),<br/>,
'Revision: ', $rev,<br/>,
'Author: ', $author,<br/>,
'Date: ', $date)
    }
  </pre>
};
(:
 : displays a message
:)
declare function control:get-message( $message as xs:string?, $messagetype as xs:string?) as element(div )?{
  if( $message )
  then
    <div id="message-wrapper">
      <div id="message">
        <p>{control-util:decode-uri( $message )}
          <button class="btn">
          <a href="{control-util:get-url-without-msg()}">OK</a>
            <img class="small-icon" src="{$control:path || '/static/icons/open-iconic/svg/check.svg'}" alt="ok"/>
          </button>
        </p>
      </div>
      <div id="message-background" class="{$messagetype}">
      </div>
    </div>
  else()
};
(:
 : Returns a file.
 : @param  $file  file or unknown path
 : @return rest binary data
 :)
declare
%rest:path("/control/static/{$file=.+}")
%perm:allow("all")
function control:file(
$file as xs:string
) as item()+ {
  let $path := file:base-dir() || 'static/' || $file
  return
    (
    web:response-header(
    map {'media-type': web:content-type( $path )},
    map {
      'Cache-Control': 'max-age=3600,public',
      'Content-Length': file:size( $path )
    }
    ),
    file:read-binary( $path )
    )
};
(:
 : User Management main page
 : For now contains only Reset Password
 :)
declare
%rest:path("/control/user")
%rest:query-param("svnurl", "{$svnurl}")
%output:method('html')
%output:version('5.0')
function control:usermgmt($svnurl as xs:string?) as element(html) {
  <html>
    <head>
      {control-widgets:get-html-head($svnurl)}
    </head>
    <body>
      {control:get-message($control:msg, $control:msgtype),
       control-widgets:get-page-header( ),
       control-widgets:get-pw-change(),
       control-widgets:get-default-svnurl()}
    </body>
  </html>
};

(:
 : Configuration main page
 :)
declare
%rest:path("/control/config")
%rest:query-param("svnurl", "{$svnurl}")
%output:method('html')
%output:version('5.0')
function control:configmgmt($svnurl as xs:string) as element(html) {
let $auth := control-util:parse-authorization(request:header("Authorization"))
return
  <html>
    <head>
      {control-widgets:get-html-head($svnurl)
       }
    </head>
    <body>
      {control:get-message($control:msg, $control:msgtype),
       control-widgets:get-page-header( ),
       if (control-util:is-admin(map:get($auth,'username')))
       then (<div class="adminmgmt-wrapper"> {
              control-widgets:create-new-user($svnurl),
              control-widgets:customize-users($svnurl),
              control-widgets:remove-users($svnurl),
              control-widgets:create-new-group($svnurl),
              control-widgets:customize-groups($svnurl),
              control-widgets:remove-groups($svnurl),
              control-widgets:rebuild-index($svnurl, 'root'),
              control-widgets:create-btn($svnurl, 'back', true())
             }</div>,
             <div>{'session-id: '||session:id()}</div>)
       else ''}
    </body>
  </html>
};
(:
 : get pw set result
 :)
declare
%rest:path("/control/user/setpw")
%rest:query-param("svnurl", "{$svnurl}")
%output:method('html')
%output:version('5.0')
function control:setpw($svnurl as xs:string) {

let $auth := control-util:parse-authorization(request:header("Authorization")),
    $username := map:get($auth, 'username'),
    $password := map:get($auth, 'password'),
    $oldpw := request:parameter("oldpw"),
    $newpw := request:parameter("newpw"),
    $newpwre := request:parameter("newpwre"),

    (: checks if the user is logged in and provided the correct old password :)
    $iscorrectuser :=
      if ($password = $oldpw)
      then
        proc:execute( $control:htpasswd-script, ($control:htpasswd-file, 'vb', $username, $password, $control:htpasswd-group))
(:        proc:execute( 'htpasswd', ('-vb', $control:htpasswd, $username, $password)):)
      else
        element result { element error {"The provided old passwort is not correct."}, element code {1}},
    (: tries to set the new password and returns an error message if it fails :)
    $result :=
      if ($iscorrectuser/code = 0)
      then (
        if ($newpw = $newpwre)
        then
          proc:execute( $control:htpasswd-script, ($control:htpasswd-file, 'b', $username, $password, $control:htpasswd-group))
(:          (proc:execute('htpasswd', ('-b', $control:htpasswd, $username, $newpw))):)
        else
          (element result { element error {"The provided new passwords are not the same."}, element code {1}})
      )
      else ($iscorrectuser),
    $btntarget :=
      if ($result/code = 0)
      then
        ($control:siteurl || '?svnurl=' || $svnurl)
      else
        ($control:siteurl || '/user?svnurl=' || $svnurl),
    $btntext :=
      if ($result/code = 0)
      then
        ("OK")
      else
        ("Zurück")
return
  <html>
    <head>
      {control-widgets:get-html-head($svnurl)}
    </head>
    <body>
      {control-widgets:get-page-header( )}
      <div class="result">
        {$result/error}
        <br/>
         <a href="{$btntarget }">
          <input type="button" value="{$btntext}"/>
        </a>
      </div>
    </body>
  </html>
};
(:
 : get set defaultsvnurl result
 :)
declare
%rest:path("/control/user/setdefaultsvnurl")
%output:method('html')
%output:version('5.0')
function control:setdefaultsvnurl() {

let $auth := control-util:parse-authorization(request:header("Authorization")),
    $username := map:get($auth, 'username'),
    $defaultsvnurl := request:parameter("defaultsvnurl"),
    $file := $control:mgmtdoc,
    $updated-access := $file update {delete node //control:rels/control:rel[control:user = $username][control:defaultsvnurl]}
                             update {insert node element rel {element defaultsvnurl {$defaultsvnurl},
                                                              element user {$username}} into .//control:rels},
    $result := file:write("basex/webapp/control/"||$control:mgmtfile, $updated-access),
    $writetofile := control:writeauthtofile($updated-access)
return
  web:redirect($control:siteurl || '/user?msg=' || encode-for-uri(control-i18n:localize('updated', $control:locale )) || '&amp;msgtype=info' )
};
(:
 : set group result
 :)
declare
%rest:path("/control/user/setgroups")
%rest:query-param("svnurl", "{$svnurl}")
%output:method('html')
%output:version('5.0')
function control:setgroups($svnurl as xs:string) {

let $auth := control-util:parse-authorization(request:header("Authorization")),
    $username := map:get($auth, 'username'),
    
    $groups := request:parameter("groups"),
    $selected-user := request:parameter("users"),
    
    $file := $control:mgmtdoc,
    
    $added-rel := for $group in $groups 
                   return element rel {
                            element user {$selected-user},
                            element group {$group}
                          },
    $updated-access := $file update {delete node //control:rels//control:rel
                                          [control:group]
                                          [control:user = $selected-user]}
                                       update {insert nodes $added-rel into //control:rels},
    $result :=
      if (control-util:is-admin($username))
      then (element result {attribute msg {'updated'},
                            attribute msgtype {'info'}},
            file:write("basex/webapp/control/"||$control:mgmtfile, $updated-access),
            control:writeauthtofile($updated-access))
      else element result {attribute msg {'not-admin'},
                           attribute msgtype {'error'}}
return
  web:redirect($control:siteurl || '/config?svnurl='|| $svnurl || control-util:get-message-url($result/@msg,$result/@msgtype,false(), true()))
};

(:
 : delete group result
 :)
declare
%rest:path("/control/group/delete")
%rest:query-param("svnurl", "{$svnurl}")
%output:method('html')
%output:version('5.0')
function control:deletegroups($svnurl as xs:string) {

let $auth := control-util:parse-authorization(request:header("Authorization")),
    $username := map:get($auth, 'username'),
    $selected-group := request:parameter("groups"),
    $file := $control:mgmtdoc,
    $updated-access := $file update {delete node //control:rels/control:rel[control:user][control:group = $selected-group]}
                             update {delete node //control:rels/control:rel[control:repo][control:group = $selected-group]}
                             update {delete node //control:groups/control:group[control:name = $selected-group]},
    $result :=
      if (control-util:is-admin($username))
      then (element result {attribute msg {'group-deleted'},
                            attribute msgtype {'info'}},
            file:write("basex/webapp/control/"||$control:mgmtfile, $updated-access),
            control:writeauthtofile($updated-access))
      else element result {attribute msg {'not-admin'},
                           attribute msgtype {'error'}}
return
  web:redirect($control:siteurl || '/config?svnurl='|| $svnurl || control-util:get-message-url($result/@msg,$result/@msgtype,false(), true()))
};
(:
 : set access result
 :)
declare
%rest:path("/control/group/setaccess")
%rest:query-param("svnurl", "{$svnurl}")
%rest:query-param("file", "{$file}")
%output:method('html')
%output:version('5.0')
function control:setaccess($svnurl as xs:string, $file as xs:string) {
let $auth := control-util:parse-authorization(request:header("Authorization")),
    $username := map:get($auth, 'username'),
    $selected-group := request:parameter("groups"),
    $selected-permission := request:parameter("access"),
    $selected-repo := tokenize(svn:info($svnurl, $control:svnauth)/*:param[@name = 'root-url']/@value,'/')[last()],
    $selected-filepath := replace(
                                string-join(
                                  ($svnurl,$file)
                                  ,'/')
                                ,svn:info($svnurl, $control:svnauth)/*:param[@name = 'root-url']/@value ||'/',''),
    $control-file := $control:mgmtdoc,
    $updated-access := $control-file update {delete node //control:rels/control:rel
                                      [control:repo = $selected-repo]
                                      [control:file = $selected-filepath]
                                      [control:group = $selected-group]}
                             update {insert node element rel {
                                      element group {$selected-group},
                                      element repo {$selected-repo},
                                      element file {$selected-filepath},
                                      element permission {$selected-permission}} into .//control:rels},
    $result :=
      if (control-util:is-admin($username))
      then (element result {attribute msg {'updated'},
                            attribute msgtype {'info'}},
            file:write("basex/webapp/control/"||$control:mgmtfile, $updated-access),
            control:writeauthtofile($updated-access))
      else element result {attribute msg {'not-admin'},
                           attribute msgtype {'error'}}
return
  web:redirect($control:siteurl || '/config?svnurl='|| $svnurl || control-util:get-message-url($result/@msg,$result/@msgtype,false(), true()))
};

(:
 : Conversion mgmt page
 :)
declare
%rest:path("/control/convert")
%rest:query-param("svnurl", "{$svnurl}")
%rest:query-param("file", "{$file}")
%rest:query-param("type", "{$type}")
%output:method('html')
%output:version('5.0')
function control:convert($svnurl as xs:string, $file as xs:string, $type as xs:string) as element(html) {
  <html>
    <head>
      {control-widgets:get-html-head($svnurl)}
    </head>
    <body>
      {control:get-message($control:msg, $control:msgtype),
       control-widgets:get-page-header(),
       control-widgets:manage-conversions($svnurl, $file, $type)}
    </body>
  </html>
};

(:
 : start conversion result
 :)
declare
%rest:path("/control/convert/start")
%rest:query-param("svnurl", "{$svnurl}")
%rest:query-param("file", "{$file}")
%rest:query-param("type", "{$type}")
%output:method('html')
%output:version('5.0')
function control:startconversion($svnurl as xs:string, $file as xs:string, $type as xs:string) {
let $auth := control-util:parse-authorization(request:header("Authorization")),
    $username := map:get($auth, 'username'),
    $selected-group := request:parameter("groups"),
    $selected-permission := request:parameter("access"),
    $selected-repo := tokenize(svn:info($svnurl, $control:svnauth)/*:param[@name = 'root-url']/@value,'/')[last()],
    $selected-filepath := replace(
                                string-join(
                                  ($svnurl,$file)
                                  ,'/')
                                ,svn:info($svnurl, $control:svnauth)/*:param[@name = 'root-url']/@value ||'/',''),
    $started-conversion := control-util:start-new-conversion($svnurl, $file, $type),
    $control-file := $control:mgmtdoc,
    $updated-access := $control-file update {delete node //control:conversion
                                                             [control:file = $file]
                                                             [control:svnurl = $svnurl]
                                                             [control:type = $type]}
                                     update {insert node $started-conversion into .//control:conversions},
    $result :=
      if ($started-conversion/*:status/text() eq 'uploaded')
      then (element result {attribute msg {'started'},
                            attribute msgtype {'info'}},
            file:write("basex/webapp/control/"||$control:mgmtfile, $updated-access),
            control:writeauthtofile($updated-access))
      else element result {attribute msg {string-join($started-conversion//text(),',')},
                           attribute msgtype {'error'}}
return
  web:redirect($control:siteurl || '/convert?svnurl='|| $svnurl || '&amp;file=' || $file || '&amp;type=' || $type || control-util:get-message-url($result/@msg,$result/@msgtype,false(), false()))
};

(:
 : rebuild index
 :)
declare
%rest:path("/control/config/rebuildindex")
%rest:query-param("svnurl", "{$svnurl}")
%rest:query-param("name", "{$name}")
%output:method('html')
%output:version('5.0')
function control:rebuildindex($svnurl as xs:string, $name as xs:string) {

let $auth := control-util:parse-authorization(request:header("Authorization")),
    $username := map:get($auth, 'username'),
    $result :=
      if (control-util:is-admin($username))
      then (element result {attribute msg {'index-build'},
                            attribute msgtype {'info'}},
            control-util:create-path-index($control:svnurlhierarchy, $name, $name, $control:svnurlhierarchy,''))
      else element result {attribute msg {'not-admin'},
                           attribute msgtype {'error'}}
return
  web:redirect($control:siteurl || '/config?svnurl='|| $svnurl || control-util:get-message-url($result/@msg,$result/@msgtype,false(), true()))
};

declare
%rest:path("/control/group/removepermission")
%rest:query-param("svnurl", "{$svnurl}")
%rest:query-param("file", "{$file}")
%rest:query-param("group", "{$group}")
%output:method('html')
%output:version('5.0')
function control:removepermission($svnurl as xs:string, $file as xs:string, $group as xs:string) {

let $auth := control-util:parse-authorization(request:header("Authorization")),
    $username := map:get($auth, 'username'),
    $selected-repo := tokenize(svn:info($svnurl, $control:svnauth)/*:param[@name = 'root-url']/@value,'/')[last()],
    $selected-filepath := replace(replace(replace(string-join(($svnurl,$file),'/'),'/$',''),svn:info($svnurl, $control:svnauth)/*:param[@name = 'root-url']/@value,''),'^/',''),
    $control-file := $control:mgmtdoc,
    $updated-access := $control-file update {delete node //control:rels/control:rel
                                      [control:repo = $selected-repo]
                                      [control:file = $selected-filepath]
                                      [control:group = $group]},
    $result :=
      if (control-util:is-admin($username))
      then (element result {attribute msg {'deleted'},
                            attribute msgtype {'info'}},
            file:write("basex/webapp/control/"||$control:mgmtfile, $updated-access),
            control:writeauthtofile($updated-access))
      else element result {attribute msg {'not-admin'},
                           attribute msgtype {'error'}}
return
  web:redirect($control:siteurl || '/access?svnurl='|| $svnurl || control-util:get-message-url($result/@msg,$result/@msgtype,false(), true()))
};
declare
%rest:path("/control/convert/cancel")
%rest:query-param("svnurl", "{$svnurl}")
%rest:query-param("file", "{$file}")
%rest:query-param("type", "{$type}")
%output:method('html')
%output:version('5.0')
function control:cancelconversion($svnurl as xs:string, $file as xs:string, $type as xs:string) {
let $auth       := control-util:parse-authorization(request:header("Authorization")),
    $username   := map:get($auth, 'username'),
    $conversion := control-util:get-running-conversions($svnurl, $file, $type),
    $delete     := proc:execute('curl',('-u', $control:svnusername||':'||$control:svnpassword,control-util:get-converter-function-url(control-util:get-converter-for-type($type)/@name,'delete')||'?input_file='||$file||'&amp;type='||$type)),
    $delete_res := json:parse($delete/output),
    $mgmt := $control:mgmtdoc,
    $updated-access := $mgmt update {delete node //control:conversion[control:id = $conversion/control:id]},
    $result :=
      if (xs:string(control-util:or(($delete_res/*:status/text() = 'success',matches(xs:string($delete_res/*:error/text()),'Invalid request: No such file or directory'),matches(xs:string($delete_res/*:error/text()),'Invalid request: File not found')))))
      then (element result {attribute msg {'deleted'},
                            attribute msgtype {'info'}},
            file:write("basex/webapp/control/"||$control:mgmtfile, $updated-access))
      else element result {attribute msg {string-join($delete_res//text(),',')},
                           attribute msgtype {'error'}}
return
  web:redirect($control:siteurl || '/convert?svnurl='|| $svnurl || '&amp;file='|| $file|| '&amp;type='|| $type || control-util:get-message-url($result/@msg,$result/@msgtype,false(), false()))
};
(:
 : delete user result
 :)
declare
%rest:path("/control/user/delete")
%rest:query-param("svnurl", "{$svnurl}")
%output:method('html')
%output:version('5.0')
function control:deleteuser($svnurl as xs:string) {

let $auth := control-util:parse-authorization(request:header("Authorization")),
    $username := map:get($auth, 'username'),
    $selected-user := request:parameter("users"),
    $file := $control:mgmtdoc,
    $updated-access := $file update {delete node //control:rels/control:rel[control:group][control:user = $selected-user]}
                             update {delete node //control:users/control:user[control:name = $selected-user]},
    $result :=
      if (control-util:is-admin($username))
      then (element result {attribute msg {'user-deleted'},
                            attribute msgtype {'info'}},
            file:write("basex/webapp/control/"||$control:mgmtfile, $updated-access),
            control:writeauthtofile($updated-access))
      else element result {attribute msg {'not-admin'},
                           attribute msgtype {'error'}}
return
  web:redirect($control:siteurl || '/config?svnurl='|| $svnurl || control-util:get-message-url($result/@msg,$result/@msgtype,false(), true()))
};
(:
 : create new user
 :)
declare function control:createuser-bg($newusername as xs:string, $newpassword as xs:string, $defaultsvnurl as xs:string?) {
  let $callres := proc:execute('htpasswd', ('-b', $control:htpasswd, $newusername, $newpassword)),
      $fileupdate := control-util:add-user-to-mgmt($newusername, $defaultsvnurl)
  return $callres
};
(:
 : create new user
 :)
declare
%rest:path("/control/user/createuser")
%rest:query-param("svnurl", "{$svnurl}")
%output:method('html')
%output:version('5.0')
function control:createuser($svnurl as xs:string) {
let $auth := control-util:parse-authorization(request:header("Authorization")),
    $username := map:get($auth, 'username'),
    $newusername := request:parameter("newusername"),
    $newpassword := request:parameter("newpassword"),
    $defaultsvnurl := request:parameter("defaultsvnurl"),

    $result :=
      if (control-util:is-admin($username))
      then (element result {attribute msg {'user-created'},
                            attribute msgtype {'info'}},
            control:createuser-bg($newusername, $newpassword, $defaultsvnurl))
      else element result {attribute msg {'not-admin'},
                           attribute msgtype {'error'}}
return
  web:redirect($control:siteurl || '/config?svnurl='|| $svnurl || control-util:get-message-url($result/@msg,$result/@msgtype,false(), true()))
};
(:
 : create new group
 :)
declare function control:creategroup-bg($newgroupname as xs:string?,$newgroupreporegex as xs:string?) {
let $callres := element result { element error {"Group created."}, element code {0}},
    $fileupdate := file:write("basex/webapp/control/"||$control:mgmtfile,
          let $file := $control:mgmtdoc
          return $file update {insert node element group {element name {$newgroupname}} into .//*:groups}
                       update {insert node element rel {element group {$newgroupname}, element repo {$newgroupreporegex}} into .//*:rels}
        )
return $callres
};
(:
 : create new group
 :)
declare
%rest:path("/control/group/creategroup")
%rest:query-param("svnurl", "{$svnurl}")
%output:method('html')
%output:version('5.0')
function control:creategroup($svnurl as xs:string) {
let $auth := control-util:parse-authorization(request:header("Authorization")),
    $username := map:get($auth, 'username'),
    $newgroupname := request:parameter("newgroupname"),
    $newgroupreporegex := request:parameter("newgroupname"),

    $result :=
      if (control-util:is-admin($username))
      then (element result {attribute msg {'group-created'},
                            attribute msgtype {'info'}},
            control:creategroup-bg(xs:string($newgroupname),xs:string($newgroupreporegex)))
      else element result {attribute msg {'not-admin'},
                           attribute msgtype {'error'}}
return
  web:redirect($control:siteurl || '/config?svnurl='|| $svnurl || control-util:get-message-url($result/@msg,$result/@msgtype,false(), true()))
};

(:
 : set reporegex result
 :)
declare
%rest:path("/control/group/setrepo")
%rest:query-param("svnurl", "{$svnurl}")
%output:method('html')
%output:version('5.0')
function control:setreporegex($svnurl as xs:string) {

let $auth := control-util:parse-authorization(request:header("Authorization")),
    $username := map:get($auth, 'username'),
    $reporegex := request:parameter("grouprepo"),
    $selected-group := request:parameter("groups"),
    $file := $control:mgmtdoc,
    $added-rel := element rel {
                    element group {$selected-group},
                    element repo {$reporegex}
                  },
    $updated-access := $file update {delete node //control:rels//control:rel
                                          [control:repo]
                                          [control:group = $selected-group]}
                             update {insert nodes $added-rel into //control:rels},
    $result :=
      if (control-util:is-admin($username))
      then (element result {attribute msg {'user-deleted'},
                            attribute msgtype {'info'}},
            file:write("basex/webapp/control/"||$control:mgmtfile, $updated-access),
            control:writeauthtofile($updated-access))
      else element result {attribute msg {'not-admin'},
                           attribute msgtype {'error'}}
return
  web:redirect($control:siteurl || '/config?svnurl='|| $svnurl || control-util:get-message-url($result/@msg,$result/@msgtype,false(), true()))
};
(:
 : get groups for user
 :)
declare
%rest:path("/control/user/getgroups")
%rest:query-param("username", "{$username}")
%output:method('xml')
function control:getusergroups($username as xs:string) {
let $usergroups :=
      $control:access/control:rels/control:rel[control:user][control:group][control:user = $username]
return
<response>
  {$usergroups}
</response>
};
(:
 : get glob for group
 :)
declare
%rest:path("/control/group/getglob")
%rest:query-param("groupname", "{$groupname}")
%output:method('xml')
function control:getgrouprepoglob($groupname as xs:string) {
let $groupglob :=
      $control:access/control:rels/control:rel[control:group][control:repo][control:group = $groupname]
return
<response>
  {$groupglob}
</response>
};

declare 
function control:writeauthtofile($access) {
  file:write($control:svnauthfile,control:writetoauthz($access))
};

declare
function control:writetoauthz($access) {
  concat(control-util:writegroups($access),
    $control:nl,
    '[/]',
    $control:nl,
    '* = ',$control:default-permission,$control:nl,
    '@admin = rw',$control:nl,
    string-join(
      for $repo in file:list($control:svnbasewerke) (:repos:)
      return 
        let $repo-groups := 
          for $group in $access//control:groups/control:group (:groups:)
          let $permission := control-util:get-permission-for-group($group/control:name, replace($repo,'/',''), $access)
          where $access//control:rels/control:rel[control:user][control:group = $group] (: not empty groups:)
          return element permission {element group {$group/control:name},
                                     element permission {$permission}}
        return if ($repo-groups[permission != ''][permission != $control:default-permission])
               then
                  concat('[', replace($repo,'/',''),':/]',$control:nl,
                  string-join(
                    for $group in $repo-groups[permission != ''] (:groups:)
                    return
                      if ($group/permission != $control:default-permission)
                      then concat('@',$group/group,'=',$group/permission,$control:nl)
                  ),$control:nl)
    ),
    string-join(
      for $a in $access//control:rels/control:rel[control:repo][control:group][control:permission][control:file != '']
      let $selected-permission := if ($a/control:permission = 'none') then ''
                        else if ($a/control:permission = 'read') then 'r'
                        else if ($a/control:permission = 'write') then 'rw'
      return concat(
               '[',
               $a/control:repo,':/',
               replace($a/control:file,'^/',''),
               ']',
               $control:nl,
               concat('@',$a/control:group),' = ', $selected-permission,$control:nl
             )
    )
    )
};

declare
%rest:path("/control/testipopesti")
%rest:query-param("svnurl", "{$svnurl}")
%output:method('xml')
function control:testipopesti($svnurl as xs:string) {
<doc>
<e>{control-util:get-local-path($svnurl)}</e>
<e>{(db:attribute('INDEX', control-util:get-local-path($svnurl), 'svnpath'))[1]/../@virtual-path}</e>
<e>{(db:attribute('INDEX', control-util:get-local-path($svnurl), 'path'))[1]/../@mount-point}</e>
<e>{$svnurl ! control-util:get-virtual-path(.)}</e>
<e>{$svnurl ! control-util:get-local-path(.) ! (db:attribute('INDEX', ., 'svnpath'))[1]/../@virtual-path}</e>
</doc>
};