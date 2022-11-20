module namespace control-widgets = 'http://transpect.io/control/util/control-widgets';
import module namespace svn = 'io.transpect.basex.extensions.subversion.XSvnApi';
import module namespace control = 'http://transpect.io/control' at '../control.xq';
import module namespace control-i18n = 'http://transpect.io/control/util/control-i18n' at 'control-i18n.xq';
import module namespace control-util = 'http://transpect.io/control/util/control-util' at 'control-util.xq';
declare namespace c = 'http://www.w3.org/ns/xproc-step';

(: 
 : gets the html head 202202181307
 :)
declare function control-widgets:get-html-head($title-text as xs:string?) as element()+ {
  <meta charset="utf-8"></meta>,
  <title>{$title-text} – transpect control</title>,
  <script src="{ $control:siteurl || '/static/js/control.js'}" type="text/javascript"></script>,
  <link rel="stylesheet" type="text/css" href="{ $control:siteurl || '/static/style.css'}"></link>
};

declare function control-widgets:get-page-footer( ) as element(footer) {
  <footer>
  </footer>
};

(:
 :
 :)
declare function control-widgets:manage-conversions($svnurl as xs:string, $file as xs:string, $type as xs:string){
  let $repo := tokenize(svn:info($svnurl, $control:svnauth)/*:param[@name = 'root-url']/@value,'/')[last()],
      $filepath := replace(
                     replace(
                       string-join(
                         ($svnurl,$file),'/'),'/$','')
                         ,svn:info(
                           $svnurl, $control:svnauth)/*:param[@name = 'root-url']/@value
                         ,''),
      $conversion := control-util:get-running-conversions($svnurl, $file, $type)[1]
  return
    <div class="conversion-widget">
      <div class="adminmgmt">
        <h2> {control-i18n:localize('convert-title', $control:locale ) || ' ' || $filepath }</h2>
        <div id="streamed-data" class="hidden">
          {for $c in control-util:get-running-conversions($svnurl, $file, $type)
           return control-util:update-conversion($c/control:id),
           control-util:get-running-conversions($svnurl, $file, $type)}
        </div>
      </div>
      {if ($conversion)
       then
      (<div class="adminmgmt">
        <h2>{control-i18n:localize('status', $control:locale )}</h2>
        <div>{$conversion/control:status,
              if ($conversion) then element a {attribute class {"delete"},
                                               attribute href {$control:siteurl||"/convert/cancel?svnurl="||$svnurl||"&amp;file="||$file||"&amp;type="||$type},
                                               text {"&#x1f5d1;"}}}</div>
      </div>,
      <div class="adminmgmt">
        <h2>{control-i18n:localize('messages', $control:locale )}</h2>
        <div class="textlist">{for $m in $conversion/control:messages/*
              return element div {text {$m/text()}}}</div>
      </div>,
      <div class="adminmgmt">
        <h2>{control-i18n:localize('result_files', $control:locale )}</h2>
        <div>{for $f in $conversion/control:result_files/*
              return element div {element a {attribute href {$control:siteurl||"/download-conversion-result?svnurl="||$svnurl||"&amp;file="||$file || "&amp;type="||$type||"&amp;result_file="||$f/@name},
                                             text {$f/@name}}}}
        </div>
      </div>)}
      <div class="adminmgmt">
        <h2> {control-i18n:localize(if ($conversion) then 'restart_conversion' else 'start_conversion', $control:locale ) || ' ' || $filepath }</h2>
        <form action="{$control:siteurl}/convert/start?svnurl={$svnurl}&amp;file={$file}&amp;type={$type}" method="POST" enctype="application/x-www-form-urlencoded" autocomplete="off">
          <div class="start-new-conversion">
            <input type="submit" value="{control-i18n:localize('start_conversion', $control:locale)}"/>
          </div>
        </form>
      </div>
      {control-widgets:create-btn($svnurl, 'back', true())}
    </div>
};

(:
 : get the fancy page head
 :)
declare function control-widgets:get-page-header() as element(header) {
  let $credentials := request:header("Authorization")
                    => substring(6)
                    => xs:base64Binary()
                    => bin:decode-string()
                    => tokenize(':'),
    $username := $credentials[1]
  return
    <header class="page-header">
      <div class="header-wrapper">
        <div id="logo">
          <a href="{ $control:siteurl }">
            <img src="{ $control:siteurl || '/static/icons/transpect.svg'}" alt="transpect logo"/>
          </a>
        </div>
        <h1><a href="{ $control:siteurl }"><span class="thin">transpect</span>control</a></h1>
      </div>
      <div class="nav-wrapper">
        <nav class="nav">
          <ol class="nav-ol">
            <li class="nav-tab"><a href="{ $control:siteurl|| '?svnurl=' || $control:svnurlhierarchy }">{control-i18n:localize('files', $control:locale)}</a></li>
            <li class="nav-tab">{
              if (control-util:is-admin($username))
              then 
                <a href="{$control:siteurl ||  '/config?svnurl=' || $control:svnurl}">{control-i18n:localize('configuration', $control:locale)}</a>
            }
            </li>
          </ol>
          <ol class="username">
            <li class="nav-tab"><a href="{$control:siteurl ||  '/user'}">{$username}</a></li>
          </ol>
        </nav>
      </div>
    </header>
};

declare function control-widgets:get-svnhome-button( $svnurl as xs:string, $control-dir as xs:string, $auth as map(*) ) as element(div){
  <div class="home">
    <a href="{(:concat($control-dir,
                     '?svnurl=',
                     $control:svnbase):)
               concat($control-dir,
               '?svnurl=',
               svn:info($svnurl, $auth)/*:param[@name eq 'root-url']/@value)
              }">
      <button class="home action btn">
        <img class="small-icon" src="{$control-dir || '/static/icons/open-iconic/svg/home.svg'}" alt="home"/>
      </button>
    </a>
  </div>
};

declare function control-widgets:get-back-to-svndir-button( $svnurl as xs:string, $control-dir as xs:string ) as element(div){
  <div class="back">
    <a href="{$control:siteurl || '?svnurl=' || $svnurl}">
      <button class="back action btn">
        <img class="small-icon" src="{$control-dir || '/static/icons/open-iconic/svg/chevron-left.svg'}" alt="back"/>
      </button>
    </a>
  </div>
};

declare function control-widgets:rebuild-index($svnurl as xs:string,
                                               $name as xs:string) as element(div){
  <div class="adminmgmt">
    <h2>{control-i18n:localize('rebuildindex', $control:locale)}</h2>
    <form action="{$control:siteurl}/config/rebuildindex?svnurl={$svnurl}&amp;name={$name}">
      <input type="submit" value="{control-i18n:localize('rebuildindexbtn', $control:locale)}" />
    </form>
  </div>
};

declare function control-widgets:create-btn($svnurl as xs:string, $text as xs:string, $localize as xs:boolean) as element(div) {
  <div class="adminmgmt">
    <form action="{$control:siteurl}">
      <input type="submit" value="{if ($localize) then control-i18n:localize($text, $control:locale)
                                                  else $text}" />
      <input type="hidden" name="svnurl" value="{$svnurl}"/>
    </form>
  </div>
};

(:
 : get file action dropdown button
 :)
declare function control-widgets:get-file-action-dropdown( $svnurl as xs:string, $file) as element(details){
  <details class="file action dropdown autocollapse">
    <summary class="btn">
      {control-i18n:localize('actions', $control:locale)}<span class="spacer"/>▼
    </summary>
    <div class="invisible">{$file}</div>
    <div class="dropdown-wrapper">
      <ul>{
        if ($file[@mount])
        then (
          <li>
           <a class="btn" href="{$control:path || '/external/remove?svnurl=' || $svnurl || '&amp;mount=' || $file/@mount }">{control-i18n:localize('remove-external', $control:locale)}</a>
          </li>,
          <li>
           <a class="btn" href="{$control:path || '/external/change-url?svnurl=' || $svnurl || '&amp;mount=' || $file/@mount }">{control-i18n:localize('change-url', $control:locale)}</a>
          </li>,
          <li>
           <a class="btn" href="#" onclick="{'showLogForm(''' || $file/@url || ''', '''', ''' || $control:path || ''')' }">{control-i18n:localize('showLog', $control:locale)}</a>
          </li>,
          <li>
           <a class="btn" href="#" onclick="{'showInfoForm(''' || $svnurl || ''', ''' || $file || ''', ''' || $control:path || ''')' }">{control-i18n:localize('showInfo', $control:locale)}</a>
          </li>,
          <li>
           <a class="btn" href="#" onclick="{'createChangeMountForm(''' || $svnurl || ''', ''' || $file/@mount || ''', ''' || $file/@url || ''', ''' || $control:path || ''')' }">{control-i18n:localize('change-mountpoint', $control:locale)}</a>
          </li>
        ) else (
          <li>
           <a class="btn" href="#" onclick="{'createRenameForm(''' || $svnurl || ''', ''' || $file/@name || ''', ''' || $control:path || ''')' }">{control-i18n:localize('rename', $control:locale)}</a>
          </li>,
          <li>
           <a class="btn" href="#" onclick="{'showLogForm(''' || $svnurl || ''', ''' || $file/@name || ''', ''' || $control:path || ''')' }">{control-i18n:localize('showLog', $control:locale)}</a>
          </li>,
          <li>
           <a class="btn" href="#" onclick="{'showInfoForm(''' || $svnurl || ''', ''' || $file/@name || ''', ''' || $control:path || ''')' }">{control-i18n:localize('showInfo', $control:locale)}</a>
          </li>,
          <li>
            <a class="btn" href="{$control:path || '/copy?svnurl=' || $svnurl || '&amp;action=copy&amp;file=' || $file/@name }">{control-i18n:localize('copy', $control:locale)}</a>
          </li>,
          <li>
            <a class="btn" href="{$control:path || '/access?svnurl=' || $svnurl || '&amp;action=access&amp;file=' || $file/@name }">{control-i18n:localize('access', $control:locale)}</a>
          </li>,
          <li>
            <a class="btn" href="{$control:path || '/move?svnurl=' || $svnurl || '&amp;action=move&amp;file=' || $file/@name }">{control-i18n:localize('move', $control:locale)}</a>
          </li>,
          <li>
            <a class="btn" href="{$control:path || '/delete?svnurl=' || $svnurl || '&amp;file=' || $file/@name || '&amp;action=delete'}">{control-i18n:localize('delete', $control:locale)}</a>
          </li>,
          if (control-util:is-file($file/@name))
          then (
            <li>
              <a class="btn" href="{$control:path || '/download-file?svnurl=' || $svnurl || '&amp;file=' || $file/@name}">{control-i18n:localize('download', $control:locale)}</a>
            </li>,
          for $c in control-util:get-converters-for-file($file/@name)
          let $type := $control:converters//control:type[@type = $c]
          return 
            <li>
              <a class="btn" href="{$control:path || '/convert?svnurl=' || $svnurl || '&amp;file=' || $file/@name || '&amp;type=' || $c}">{control-i18n:localize(xs:string($type/@text), $control:locale)}</a>
            </li>
          )
        )
      }</ul>
    </div>
  </details>
};

(:
 : use request parameter and perform file action.
 :)
declare function control-widgets:manage-actions( $svnurl as xs:string, $dest-svnurl as xs:string?, $action as xs:string, $file as xs:string ) {
  if($action = ('copy', 'move')) 
      then control-widgets:display-window( $svnurl, $dest-svnurl, $action, $file )
    else if( $action = 'do-copy' )
      then svn:copy( $svnurl, 
                     $control:svnauth, 
                     substring-after( $file, $svnurl ), substring-after( $dest-svnurl, $svnurl ), 'copy' )
    else () (: tbd :)
};

(:
 : display window
 :)
declare function control-widgets:display-window( $svnurl as xs:string, $dest-svnurl as xs:string?, $action as xs:string, $file as xs:string ) as element(div)+ {
  <div class="transparent-bg"></div>,
  <div class="transparent-fg">
    <div class="window-fg">
        { if($action = ('copy', 'move')) 
          then control-widgets:choose-directory( $svnurl, $dest-svnurl, 'do-' || $action, $file )
          else()
        }
    </div>
  </div>
};

(:
 : displays window to choose directory, usually needed for performing copy or delete actions 
 :)
declare function control-widgets:choose-directory( $svnurl as xs:string, $dest-svnurl as xs:string?, $action as xs:string, $file as xs:string ) as element(div) {
  <div class="choose-directory">
    <div class="window-actions"><a class="window-action close" href="{ $control:siteurl || '?svnurl=' || $svnurl }">&#x2a2f;</a></div>
    <h2>{ control-i18n:localize('choose-dir', $control:locale) }</h2>
    <div class="directory-list table">
      <div class="table-body">
      { for $files in svn:list(control-util:path-parent-dir( $svnurl ), $control:svnusername, $control:svnpassword, false())[local-name() ne 'errors']
        return 
            <div class="table-row directory-entry {local-name( $files )}">
              <div class="icon table-cell"/>
              <div class="name parentdir table-cell">
                <a href="{$control:siteurl || '/' || $action || '?svnurl=' || $svnurl || '&amp;dest-svnurl=' || control-util:path-parent-dir( $dest-svnurl ) || '&amp;action=' || $action || '&amp;file=' || $file }">..</a></div>
              </div>,
              for $files in svn:list( $dest-svnurl, $control:svnauth, false())/*
              order by lower-case( $files/@name )
              order by $files/local-name()
              let $href := $control:siteurl || '/' || $action || '?svnurl=' || $svnurl || '&amp;dest-svnurl=' || $dest-svnurl || '/' || $files/@name || '&amp;action=' || $action || '&amp;file=' || $file
              return
                if( $files/local-name() eq 'directory' )
                then 
                  <div class="table-row directory-entry {local-name( $files )}">
                    <div class="table-cell icon">
                      <a href="{$href}">
                        <img src="{(concat( $control:path,
                                            '/../',
                                            control-util:get-mimetype-url(
                                                                          if( $files/local-name() eq 'directory') 
                                                                          then 'folder'
                                                                          else tokenize( $files/@name, '\.')[last()]
                                                                         )
                                    )
                             )}" alt="" class="file-icon"/>
                      </a>
                    </div>
                    <div class="name table-cell">
                      <a href="{$href}">{xs:string( $files/@name )}</a>
                    </div>
                    <div class="action table-cell">
                      { control-widgets:get-choose-directory-button( $svnurl, 'do-copy', $file, $dest-svnurl || '/' || $files/@name ) }
                    </div>
                  </div>
              else ()
      }
      </div>
    </div>
  </div>
};

declare function control-widgets:get-choose-directory-button( $svnurl as xs:string, $action as xs:string, $file as xs:string, $dest-svnurl as xs:string) as element(div){
  <div class="home">
    <a href="{ $control:path || '/..?svnurl=' || $svnurl || '&amp;action=' || $action || '&amp;file=' || $file || '&amp;dest-svnurl=' || $dest-svnurl }">
      <button class="select action btn">
        <img class="small-icon" src="{$control:path || '/../static/icons/open-iconic/svg/check.svg'}" alt="select"/>
        <span class="spacer"/>{control-i18n:localize('select', $control:locale )}
      </button>
    </a>
  </div>
};

(:
 : returns a html directory listing
:)
declare function control-widgets:get-dir-list( $svnurl as xs:string, $control-dir as xs:string, $is-svn as xs:boolean, $auth as map(*)) as element(div) {
  <div class="directory-list-wrapper">
  {control-widgets:get-dir-menu( $svnurl, $control-dir, $auth )}
    <div class="directory-list table">
       {(svn:list( $svnurl, $auth, true())/*,
           control-util:parse-externals-property(svn:propget($svnurl, $auth, 'svn:externals', 'HEAD')))}
      <div class="table-body">
        {control-widgets:list-dir-entries( $svnurl, $control-dir, map{'show-externals': true()})}
      </div>
    </div>
  </div>
};

declare function control-widgets:create-infobox(){
  <div id="infobox" class="infobox" style="visibility:hidden">
    <div class="header">
      <div class="heading"></div>
      <div class="closebutton" onclick="closebox(); return false">X</div>
    </div>
    <div class="content"></div>
  </div>
};

(:
 : returns controls to modify access to directory
:)
declare function control-widgets:file-access( $svnurl as xs:string, $file as xs:string ) as element(div) {
  let $repo := tokenize(svn:info($svnurl, $control:svnauth)/*:param[@name = 'root-url']/@value,'/')[last()],
      $filepath := replace(
                     replace(
                       string-join(
                         ($svnurl,$file),'/'),'/$','')
                         ,svn:info(
                           $svnurl, $control:svnauth)/*:param[@name = 'root-url']/@value
                         ,'')
  return
    <div class="access-widget">
      <div class="adminmgmt">
        <h2> {control-i18n:localize('perm-title', $control:locale ) || ' ' || $filepath }</h2>
        <div id="streamed-data" class="hidden">
          {control-util:get-permissions-for-file($svnurl, $file, $control:access)}
        </div>
        <div class="table">
          {control-i18n:localize('existingrights', $control:locale )}
            <div class="table-body">
              <div class="table-row">
                <div class="table-cell">{control-i18n:localize('group', $control:locale )}</div>
                <div class="table-cell">{control-i18n:localize('permission', $control:locale )}</div>
                <div class="table-cell">{control-i18n:localize('implicit', $control:locale )}</div>
                <div class="table-cell">{control-i18n:localize('delete', $control:locale )}</div>
              </div>
            </div>
          {for $access in control-util:get-permissions-for-file($svnurl, $file,$control:access)
           return <div class="table-row">
                    <div class="table-cell">{$access/g}</div>
                    <div class="table-cell">{$access/p/text()}</div>
                    {if ($access/i = true())
                    then
                      <div class="table-cell">implicit</div>
                    else
                     (<div class="table-cell">explicit</div>,
                      <div class="table-cell"><a class="delete" href="{$control:siteurl}/group/removepermission?svnurl={$svnurl}&amp;file={$file}&amp;group={$access/*:g/text()}">&#x1f5d1;</a></div>)
                    }
                  </div>}
        </div>
      </div>
      <div class="adminmgmt">
        <h2> {control-i18n:localize('set-perm', $control:locale ) || ' ' || $filepath }</h2>
        <form action="{$control:siteurl}/group/setaccess?svnurl={$svnurl}&amp;file={$file}" method="POST" enctype="application/x-www-form-urlencoded" autocomplete="off">
          <div class="add-new-access">
            <div class="form">
              <label for="groupname" class="leftlabel">{concat(control-i18n:localize('selectgroup', $control:locale),':')}</label>
              <select name="groups" id="groupselect">
                {control-widgets:get-groups( $svnurl )}
              </select>
            </div>
            <div class="form">
              <label for="access" class="leftlabel">{concat(control-i18n:localize('selectdiraccess', $control:locale),':')}</label>
              <select name="access" id="readwrite">
                <option value="none">{control-i18n:localize('none', $control:locale)}</option>
                <option value="read">{control-i18n:localize('read', $control:locale)}</option>
                <option value="write">{control-i18n:localize('write', $control:locale)}</option>
              </select>
            </div>
            <br/>
            <input type="submit" value="{control-i18n:localize('submit', $control:locale)}"/>
          </div>
        </form>
      </div>
      {control-widgets:create-btn($svnurl, 'back', true())}
    </div>
};

(:
 : get dir menu
 :)
declare function control-widgets:get-dir-menu( $svnurl as xs:string, $control-dir as xs:string, $auth as map(*) ) {
  <div class="dir-menu">
    <div class="dir-menu-left">
      {control-widgets:get-svnhome-button( $svnurl, $control-dir, $auth )}
      <div class="breadcrumb">
        {control-util:get-breadcrumb-links($svnurl)}
      </div>
      {control-widgets:create-dir-form( $svnurl, $control-dir )}
    </div>
    <div class="dir-menu-right">
      {control-widgets:get-dir-actions( $svnurl, $control-dir )}
    </div>
  </div>
};

(:
 : get action buttons to add new files, create dirs etc.
 :)
declare function control-widgets:get-dir-actions( $svnurl as xs:string, $control-dir as xs:string?) as element(div )* {
  <div class="directory-actions">
    <a href="{$control:siteurl||'/new-file?svnurl='||$svnurl}">
      <button class="new-file action btn">
        <img class="small-icon" src="{$control-dir || '/static/icons/open-iconic/svg/cloud-upload.svg'}" alt="new-file"/><span class="spacer"/>
        {control-i18n:localize('upload', $control:locale )}
      </button>
    </a>
    <a href="#" onclick="reveal('create-dir-form-wrapper'); false;">
      <button class="create-dir action btn" >
        <img class="small-icon" src="{$control-dir || '/static/icons/open-iconic/svg/folder.svg'}" alt="new-file"/><span class="spacer"/>
          {control-i18n:localize('create-dir', $control:locale )}
      </button>
    </a>
    <a href="control/download?svnurl={$svnurl}">
      <button class="download action btn">
        <img class="small-icon" src="{$control-dir || '/static/icons/open-iconic/svg/cloud-download.svg'}" alt="new-file"/><span class="spacer"/>
          {control-i18n:localize('download', $control:locale )}
      </button>
    </a>
  </div>
};

(:
 : provide directory listing
 :)
declare function control-widgets:list-dir-entries( $svnurl as xs:string,
                                           $control-dir as xs:string,
                                           $options as map(xs:string, item()*)?) as element(div )* {
  control-widgets:get-dir-parent( $svnurl, $control-dir, '' ),
  let $filename-filter-regex as xs:string? := $options?filename-filter-regex,
      $dirs-only as xs:boolean? := $options?dirs-only = true(),
      $add-query-params as xs:string? := $options?add-query-params,
      $show-externals as xs:boolean? := $options?show-externals = true(),
      $credentials := request:header("Authorization")
                    => substring(6)
                    => xs:base64Binary()
                    => bin:decode-string()
                    => tokenize(':'),
      $username := $credentials[1],
      $auth := map{'username':$credentials[1],'cert-path':'', 'password': $credentials[2]}
  return
  for $files in (
    svn:list( $svnurl, $auth, true())/*,
    if ($show-externals) then
      control-util:parse-externals-property(svn:propget($svnurl, $auth, 'svn:externals', 'HEAD'))
    else ()
  )
  order by lower-case( $files/(@name | @mount) )
  order by $files/local-name()
  let $href := if ($files/self::external)
               then 
                 if (starts-with($files/@url, 'https://github.com/'))
                 then replace($files/@url, '/[^/]+/?$', '/')
                 else $control:siteurl || '?svnurl=' || $files/@url || $add-query-params
               else if($files/local-name() eq 'directory')
                    then $control:siteurl || '?svnurl=' || replace($svnurl,'/$','') || '/' || $files/@name 
                      || $add-query-params
                    else $svnurl || '/' || $files/@name
  return
    if(    not($dirs-only and $files/local-name() eq 'file')
       or  not(matches($files/@name, ($filename-filter-regex, '')[1])))
    then 
    <div class="table-row directory-entry {local-name( $files )}">
      <div class="table-cell icon">
        <a href="{$href}">
          <img src="{(concat( $control-dir,
                             '/',
                             control-util:get-mimetype-url(
                                       if( $files/local-name() eq 'directory') 
                                       then 'folder'
                                       else if ($files/self::external)
                                            then 'external'
                                            else tokenize( $files/@name, '\.')[last()]
                                       )
                      )
               )}" alt="" class="file-icon"/>
        </a>
      </div>
      <div class="name table-cell">
        <a href="{ if ($files/local-name() eq 'file') then $control:path || '/download-file?svnurl=' || $svnurl || '&amp;file=' || $files/@name else $href}" id="direntry-{xs:string( $files/(@name | @mount) )}">{xs:string( $files/(@name | @mount) )}</a></div>
      <div class="author table-cell">{xs:string( $files/@author )}</div>
      <div class="date table-cell">{xs:string( $files/@date )}</div>
      <div class="revision table-cell">{xs:string( $files/@revision )}</div>
      <div class="size table-cell">{$files/@size[$files/local-name() eq 'file']/control-util:short-size(.)}</div>
      <div>{svn:info($svnurl,
                     $auth)/*:param[@name eq 'root-url']/@value
                    }</div>
      <div class="action table-cell">{if (control-util:get-rights($username, xs:string($files/@name)) = "write") 
                                      then control-widgets:get-file-action-dropdown( ($svnurl, string($files/@url))[1], $files ) 
                                      else ""}</div>
    </div> 
    else ()
};

(:
 : provides a row in the html direcory listing 
 : with the link to the parent directory
:)
declare function control-widgets:get-dir-parent( $svnurl as xs:string, $control-dir as xs:string, $repopath as xs:string? ) as element(div )* {
  let $new-svnurl := control-util:path-parent-dir($svnurl),
      $new-repopath := if ($repopath!= '') then replace($repopath,'/?[^/]+/?$','') else '',
      $virtual-path := $control:index//*[@svnpath = control-util:get-local-path($svnurl)],
      $path := (request:parameter('from'), svn:list(control-util:path-parent-dir( $svnurl ), $control:svnauth, false())/self::c:files/@*:base)[1]
  return 
    <div class="table-row directory-entry">
      <div class="icon table-cell"/>
      { if ($new-svnurl)
        then 
          <div class="name parentdir table-cell">
            <a href="{$control-dir || '?svnurl=' || $new-svnurl}">{if ($virtual-path/local-name() eq 'external')
                            then '←' 
                            else '..'}</a>
          </div>
          else
          <div class="name parentdir table-cell"></div>
      }
      <div class="author table-cell"/>
      <div class="date table-cell"/>
      <div class="revision table-cell"/>
      <div class="size table-cell"/>
      <div class="actions table-cell"/>
    </div>
};

declare function control-widgets:create-dir-form( $svnurl as xs:string, $control-dir as xs:string ) {
  <div id="create-dir-form-wrapper">
    <form id="create-dir-form" action="{$control:siteurl||'/create-dir?url='||$svnurl}" method="POST">
      <input type="text" id="dirname" name="dirname"/>
      <input type="hidden" name="svnurl" value="{$svnurl}" />
      <button class="btn ok" value="ok">
        OK
        <span class="spacer"/><img class="small-icon" src="{$control-dir || '/static/icons/open-iconic/svg/check.svg'}" alt="ok"/>
      </button>
    </form>
    <button class="btn cancel" value="cancel" onclick="hide('create-dir-form-wrapper')">
      Cancel
      <span class="spacer"/><img class="small-icon" src="{$control-dir || '/static/icons/open-iconic/svg/ban.svg'}" alt="cancel"/>
    </button>
  </div>
};

(:
 : return a form for creating a new user/overriding an existing one
 :)
declare function control-widgets:create-new-user($svnurl as xs:string) as element(div) {
  <div class="adminmgmt">
    <h2>{control-i18n:localize('createuser', $control:locale)}</h2>
    <form action="{$control:siteurl}/user/createuser?svnurl={$svnurl}" method="POST" enctype="application/x-www-form-urlencoded" autocomplete="off">
      <div class="createuser">
        <div class="form">
          <label for="newusername" class="leftlabel">{concat(control-i18n:localize('username', $control:locale),':')}</label>
          <input type="text" id="newusername" name="newusername" pattern="[A-Za-z0-9]+" title="Nutzen Sie nur Buchstaben und Zahlen"/>
        </div>
        <div class="form">
          <label for="newpassword" class="leftlabel">{concat(control-i18n:localize('initpw', $control:locale),':')}</label>
          <input type="password" id="newpassword" name="newpassword" autocomplete="new-password" pattern="....+" title="Bitte geben Sie mehr als 3 Zeichen ein."/>
        </div>
        <div class="form">
          <label for="defaultsvnurl" class="leftlabel">{concat(control-i18n:localize('defaultsvnurl', $control:locale),':')}</label>
          <input type="text" id="defaultsvnurl" name="defaultsvnurl" autocomplete="new-password"/>
        </div>
        <br/>
        <input type="submit" value="{control-i18n:localize('submit', $control:locale)}"/>
      </div>
    </form>
  </div>
};

(:
 : returns a form for changing the password
 :)
declare function control-widgets:get-pw-change() as element(div) {
  <div class="adminmgmt">
    <h2>{control-i18n:localize('changepassword', $control:locale)}</h2>
    <form action="{$control:siteurl}/user/setpw" method="POST" enctype="application/x-www-form-urlencoded" autocomplete="off">
      <div class="setpw">
        <div class="form">
          <label for="old-pwd" class="leftlabel">{concat(control-i18n:localize('oldpw', $control:locale),':')}</label>
          <input type="password" id="old-pwd" name="oldpw" autocomplete="new-password"/>
        </div>
        <div class="form">
          <label for="new-pwd" class="leftlabel">{concat(control-i18n:localize('newpw', $control:locale),':')}</label>
          <input type="password" id="new-pwd" name="newpw" autocomplete="new-password" pattern="....+" title="{control-i18n:localize('pwregextip', $control:locale)}"/>
        </div>
        <div class="form">
          <label for="new-pwd-re" class="leftlabel">{concat(control-i18n:localize('newpwre', $control:locale),':')}</label>
          <input type="password" id="new-pwd-re" name="newpwre" autocomplete="new-password" pattern="....+" title="{control-i18n:localize('pwregextip', $control:locale)}"/>
        </div>
        <br/>
        <input type="submit" value="{control-i18n:localize('submit', $control:locale)}"/>
      </div>
    </form>
  </div>
};

(:
 : returns a form for setting the default svnurl
 :)
declare function control-widgets:get-default-svnurl() as element(div) {
  let $credentials := request:header("Authorization")
                    => substring(6)
                    => xs:base64Binary()
                    => bin:decode-string()
                    => tokenize(':'),
      $username := $credentials[1]
  return
  <div class="adminmgmt">
    <h2>{control-i18n:localize('setdefaultsvnurl', $control:locale)}</h2>
    <form action="{$control:siteurl}/user/setdefaultsvnurl" method="POST" enctype="application/x-www-form-urlencoded" autocomplete="off">
      <div class="setdefaultsvnurl">
        <div class="form">
          <label for="defaultsvnurl" class="leftlabel">{concat(control-i18n:localize('defaultsvnurl', $control:locale),':')}</label>
          <input type="text" id="defaultsvnurl" name="defaultsvnurl" pattern=".+" autocomplete="new-password" value="{control-util:get-defaultsvnurl-from-user($username)}"/>
        </div>
        <br/>
        <input type="submit" value="{control-i18n:localize('submit', $control:locale)}"/>
      </div>
    </form>
  </div>
};

(:
 : returns a form for creating groups
 :)
declare function control-widgets:create-new-group( $svnurl as xs:string ) as element(div) {
  <div class="adminmgmt">
    <h2>{control-i18n:localize('creategroup', $control:locale)}</h2>
    <form action="{$control:siteurl}/group/creategroup?svnurl={$svnurl}" method="POST" enctype="application/x-www-form-urlencoded" autocomplete="off">
      <div class="createnewgroup">
        <div class="form">
          <label for="groupname" class="leftlabel">{concat(control-i18n:localize('groupname', $control:locale),':')}</label>
          <input type="text" id="groupname" name="newgroupname" autocomplete="new-password" pattern="[A-Za-z0-9]+" title="Nutzen Sie nur Buchstaben und Zahlen"/>
        </div>
        <div class="form">
          <label for="groupregex" class="leftlabel">{concat(control-i18n:localize('selectreporegex', $control:locale),':')}</label>
          <input type="text" id="newgroupregex" name="newgroupregex" autocomplete="new-password" pattern=".+" title="Regex darf nicht leer sein"/>
        </div>
        <br/>
        <input type="submit" value="{control-i18n:localize('submit', $control:locale)}"/>
      </div>
    </form>
  </div>
};

(:
 : returns a form for customizing groups
 :)
declare function control-widgets:customize-groups( $svnurl as xs:string ) as element(div) {
  <div class="adminmgmt">
    <h2>{control-i18n:localize('customizegroup', $control:locale)}</h2>
    <form action="{$control:siteurl}/group/setrepo?svnurl={$svnurl}" method="POST" enctype="application/x-www-form-urlencoded" autocomplete="off">
      <div class="managegroups">
        <div>
          <label for="groups" class="leftlabel">{concat(control-i18n:localize('selectgroup', $control:locale),':')}</label>
          <select name="groups" id="groupselect">
            {control-widgets:get-groups( $svnurl )}
          </select>
        </div>
        <div>
          <label for="grouprepo" class="leftlabel">{concat(control-i18n:localize('selectreporegex', $control:locale),':')}</label>
          <input type="text" id="grouprepo" name="grouprepo" autocomplete="new-password" pattern=".+" title="Regex darf nicht leer sein"/>
        </div>
        <br/>
        <input type="submit" value="{control-i18n:localize('submit', $control:locale)}"/>
      </div>
    </form>
  </div>
};

(:
 : returns a form for deleting groups
 :)
declare function control-widgets:remove-groups( $svnurl as xs:string ) as element(div) {
  <div class="adminmgmt">
    <h2>{control-i18n:localize('deletegroup', $control:locale)}</h2>
    <form action="{$control:siteurl}/group/delete?svnurl={$svnurl}" method="POST" enctype="application/x-www-form-urlencoded" autocomplete="off">
      <div class="managegroups">
        <div>
          <label for="groups" class="leftlabel">{concat(control-i18n:localize('selectgroup', $control:locale),':')}</label>
          <select name="groups" id="deletegroupselect">
            {control-widgets:get-groups( $svnurl )}
          </select>
        </div>
        <br/>
        <input type="submit" value="{control-i18n:localize('submit', $control:locale)}"/>
      </div>
    </form>
  </div>
};

(:
 : returns a form for deleting users
 :)
declare function control-widgets:remove-users( $svnurl as xs:string ) as element(div) {
  <div class="adminmgmt">
    <h2>{control-i18n:localize('deleteuser', $control:locale)}</h2>
    <form action="{$control:siteurl}/user/delete?svnurl={$svnurl}" method="POST" enctype="application/x-www-form-urlencoded" autocomplete="off">
      <div class="manageusers">
        <div>
          <label for="users" class="leftlabel">{concat(control-i18n:localize('selectuser', $control:locale),':')}</label>
          <select name="users" id="deleteuserselect">
            {control-widgets:get-users( $svnurl )}
          </select>
        </div>
        <br/>
        <input type="submit" value="{control-i18n:localize('submit', $control:locale)}"/>
      </div>
    </form>
  </div>
};

(:
 : returns the selection for users
 :)
declare function control-widgets:customize-users( $svnurl as xs:string ) as element(div) {
  <div class="adminmgmt">
    <h2>{control-i18n:localize('customizeuser', $control:locale)}</h2>
    <form action="{$control:siteurl}/user/setgroups?svnurl={$svnurl}" method="POST" enctype="application/x-www-form-urlencoded" autocomplete="off">
      <div class="manageuser">
        <div>
          <label for="users" class="leftlabel">{concat(control-i18n:localize('selectuser', $control:locale),':')}</label>
          <select name="users" id="userselect">
            {control-widgets:get-users( $svnurl )}
          </select>
        </div>
        <div>
          <label for="groups" class="leftlabel">{concat(control-i18n:localize('selectusergroup', $control:locale),':')}</label>
          <select name="groups" id="groups" multiple="true">
            {control-widgets:get-groups-and-admin( $svnurl )}
          </select>
        </div>
        <br/>
        <input type="submit" value="{control-i18n:localize('submit', $control:locale)}"/>
      </div>
    </form>
  </div>
};

(:
 : returns the selectionoptions for users
 :)
declare function control-widgets:get-users( $svnurl as xs:string ) as element(option)* {
  for $user in $control:access//control:users/control:user
  return
    <option value="{$user/control:name}">{$user/control:name}</option>
};

(:
 : returns the selectionoptions for groups (not admin)
 :)
declare function control-widgets:get-groups( $svnurl as xs:string ) as element(option)* {
  for $group in $control:access//control:groups/control:group
  where not($group/control:name = "admin")
  return
    <option value="{$group/control:name}">{$group/control:name}</option>
};

(:
 : returns the selectionoptions for groups
 :)
declare function control-widgets:get-groups-and-admin( $svnurl as xs:string ) as element(option)* {
  for $group in $control:access//control:groups/control:group
  return
    <option value="{$group/control:name}">{$group/control:name}</option>
};

(:
  returns the default search form. This function can be overridden in the configuration, in config/functions:
  <function role="search-form-widget" name="my-customization:search-form" arity="5"/>
  To do: modularize the individual search forms so that they can be assembled differently.
:)
declare function control-widgets:search-input ( $svnurl as xs:string?, $control-dir as xs:string, $auth as map(xs:string, xs:string), $params as map(*)?, $results as map(xs:string, item()*)? ) {
  <div class="form-wrapper">
    <details class="search-form">
      { if (normalize-space($params?term) or normalize-space($params?xpath))
        then attribute open { 'true' } else () }
      <summary>Full text / XPath search</summary>
      <form method="get" action="{$control-dir}/ftsearch" id="ftsearch-form">
        <div style="display:flex">
          <div class="autoComplete_wrapper" role="combobox" aria-owns="autoComplete_list" aria-haspopup="true" aria-expanded="false">
            <label for="term">Full text</label> 
            <input id="search" type="text" name="term" autocomplete="off" size="26" autocapitalize="none" 
              aria-controls="autoComplete_list" aria-autocomplete="both" value="{$params?term}" />
            <ul id="autoComplete_list" role="listbox" class="autoComplete_list" hidden=""></ul>
            { for $lang in $control:config/control:ftindexes/control:ftindex/@lang return (
                <input id="lang_{$lang}" type="checkbox" name="lang" value="{$lang}">
                {if ($params?lang = $lang or empty($params?lang)) then attribute checked { 'true' } else ()}
                </input>,
                <label for="lang_{$lang}">{string($lang)}</label>
              )
            }
            <span>    </span>
            <label for="xpath"> XPath </label>
            <input id="xpathsearch" type="text" name="xpath" autocomplete="off" size="38" autocapitalize="none" 
              value="{$params?xpath}"/><span>   </span>
            {
              if ($svnurl and not($svnurl = $control:svnurlhierarchy)) then ( 
                <input id="search_restrict_path" name="restrict_path" type="checkbox" value="true">
                  {if ($params?restrict_path) then attribute checked { 'true' } else ()}
                </input>,
                <label for="search_restrict_path">restrict to { $svnurl => control-util:get-canonical-path() }</label>
              )
              else ()
            }
            {
              if ($svnurl) then <input type="hidden" name="svnurl" value="{$svnurl}"/> else ()
            }
             <input type="submit" value="Search"/>
          </div>
        </div>
      </form>
      <details class="search-hints">
        <summary> Search hints </summary>
        <h4> Full text </h4>
        <p> You may use regex-like wildcards, such as <code>.*</code> for zero or more characters, 
        as documented for the <a href="https://docs.basex.org/wiki/Full-Text#Match_Options">BaseX
        <code>wildcards</code> option</a>. Examples: <code class="ft-fillable">combin.*</code>
        (for “combine”, “combined”, “combining”, “combinatorial”, etc.), 
        <code class="ft-fillable">.{{2,2}}treated</code> (for “untreated” and “retreated”), 
        <code class="ft-fillable">depression.{{0,2}}</code> (for “Depression” and “Depressionen”).</p>
        <p>You can click on any of the highlighted example expressions in order to use them in
        the form field. The same applies to the hihlighted XPath expressions below.</p>
        <p>In the result list, you can copy the matches’ XPaths to the clipboard (for use in oXygen etc.) by clicking on them.</p>
        <h4>XPath</h4>
        <p>The content of the XPath input field will be used as follows:</p>
        <ul>
          <li>If the expression starts with a slash and if the full text query is empty, it will be used verbatim. Example: 
          <code class="xpath-fillable">//boxed-text[contains-token(@content-type, 'box6')]</code>.
          This would be highly inefficient in combination with full text queries. Therefore,
          if the full text query field contains any text, leading slashes will be stripped from the
          XPath expression and it will be treated as in the last bullet point below, that is,
          <code class="xpath-fillable">//app[label]</code> will first be rewritten as
          <code class="xpath-fillable">app[label]</code> and then as 
          <code class="xpath-fillable">ancestor-or-self::app[label]</code>.</li>
          <li>If the expression starts with an axis (<code>preceding::</code>, <code>ancestor::</code> etc.)
          or with a dot (<code>.</code> or <code>..</code>), it will be used verbatim. Examples:
          <code class="xpath-fillable">preceding-sibling::title[matches(., '(Vorwort|Preface)')]</code>,
          <code class="xpath-fillable">../title[fn]</code>.
          The context item is the parent element of the full text match. If it is a <code>p</code> in 
          a <code>sec</code>, then the match will only appear in the results if <code>sec/title</code>
          matches the regular expression <code>(Vorwort|Preface)</code> or if contains a footnote, respectively. 
          Such a context-aware expression only makes sense if a full text query has been entered and if there are 
          full text search results.</li>
          <li>Otherwise, if the expression starts with a letter or with an asterisk, <code>ancestor-or-self::</code>
          will be prepended to the expression. Examples: 
          <code class="xpath-fillable">back</code> ⇒ <code class="xpath-fillable">ancestor-or-self::back</code>,
          <code class="xpath-fillable">sec[empty(sec)]</code> ⇒ <code class="xpath-fillable">ancestor-or-self::sec[empty(sec)]</code>,
          <code class="xpath-fillable">boxed-text//title</code> ⇒ <code class="xpath-fillable">ancestor-or-self::boxed-text//title</code>.
          Note that the latter won’t restrict the full text results to the <code>title</code> elements within a <code>boxed-text</code>
          element. It will return full text results that are in a <code>boxed-text</code> that also contains a <code>title</code>
          at arbitrary depth, not necessarily as an ancestor to the current full text search result. 
          In order to restrict the results to <code>title</code> elements within a <code>boxed-text</code>, you can 
          use <code class="xpath-fillable">title[ancestor::boxed-text]</code> (<code 
          class="xpath-fillable">ancestor-or-self::title[ancestor::boxed-text]</code>). 
          In order to find results in an <code>app</code> without a label whose title contains a digit and 
          that are not within a <code>ref</code>, you may choose
          <code class="xpath-fillable">self::*[empty(ancestor::ref)]/ancestor::app[empty(label)][matches(title, '\d')]</code>.
          Just like the “relative location 
          expressions” in the previous bullet point, these expressions only make sense for further filtering full text search
          results. 
          In order to find these apps that contain a number without full-text search, you may use
          <code class="xpath-fillable">//app[empty(label)][matches(title, '\d')]</code></li>
        </ul>
        <p>You can use (non-updating) XQuery 3.1 expressions supported by BaseX. This comprises XPath 3.1 <a 
        href="https://www.w3.org/TR/xpath-31/">expressions</a> and <a 
        href="https://www.w3.org/TR/xpath-functions-31/">functions</a>. Although newly introduced functions such as the aforementioned
        <code>contains-token()</code> are not part of XPath 2.0, you may find this <a 
        href="https://mulberrytech.com/quickref/xpath2.pdf">XPath 2.0 cheat sheet</a> handy.</p>
      </details>
    </details>
    { $results?ftxp }
    <details class="search-form">
      { if (normalize-space($params?overrides-term) or exists($params?type)) then attribute open { 'true' } else () }
      <summary>Search override files</summary>
      <form method="get" action="{$control-dir}/overrides-search" id="overrides-search-form">
        <div style="display:flex">
          <div class="autoComplete_wrapper" role="combobox" aria-owns="autoComplete_list" aria-haspopup="true" aria-expanded="false">
            { for $type in $control:config/control:also-indexable/control:file/@type return (
                <input id="type_{$type}" type="checkbox" name="type" value="{$type}">
                {if ($params?type = $type) then attribute checked { 'true' } else ()}
                </input>,
                <label for="type_{$type}">{string($type/../@description)}</label>
              )
            }
            <span>   </span>
            <label for="overrides-search">Text contains:</label> 
            <input id="overrides-search" type="text" name="overrides-term" autocomplete="off" size="26" autocapitalize="none" 
              aria-controls="autoComplete_list" aria-autocomplete="both" value="{$params?overrides-term}" />
            <ul id="autoComplete_list" role="listbox" class="autoComplete_list" hidden=""></ul>
            <span>   </span>
            {
              if ($svnurl and not($svnurl = $control:svnurlhierarchy)) then ( 
                <input id="overrides-search_restrict_path" name="restrict_path" type="checkbox" value="true">
                  {if ($params?restrict_path) then attribute checked { 'true' } else ()}
                </input>,
                <label for="search_restrict_path">restrict to { $svnurl => control-util:get-canonical-path() }</label>
              )
              else ()
            }
            {
              if ($svnurl) then <input type="hidden" name="svnurl" value="{$svnurl}"/> else ()
            }
             <input type="submit" value="Search overrides"/>
          </div>
        </div>
      </form>
    </details>
    { $results?overrides }
    <details class="search-form">
      { if (normalize-space($params?cssa-term) or exists($params?style-type)) then attribute open { 'true' } else () }
      <summary>Search CSSa styles</summary>
      <form method="get" action="{$control-dir}/cssa-search" id="cssa-search-form">
        <div style="display:flex">
          <div class="autoComplete_wrapper" role="combobox" aria-owns="autoComplete_list" aria-haspopup="true" aria-expanded="false">
            { for $style-type in ('para', 'inline', 'table', 'cell', 'object', 'layer') return (
                <input id="type_{$style-type}" type="checkbox" name="style-type" value="{$style-type}">
                {if ($params?style-type = $style-type) then attribute checked { 'true' } else ()}
                </input>,
                <label for="type_{$style-type}">{$style-type}</label>
              )
            }
            <span>   </span>
            <label for="cssa-term-search">Name contains:</label> 
            <input id="cssa-term-search" type="text" name="cssa-term" autocomplete="off" size="26" autocapitalize="none" 
              aria-controls="autoComplete_list" aria-autocomplete="both" value="{$params?cssa-term}" />
            <ul id="autoComplete_list" role="listbox" class="autoComplete_list" hidden=""></ul>
            <span>   </span>
            <label for="group">Group by:</label> 
            <select name="group" id="group">
              <option value="style-hierarchy">{ 
                if ($params?group = 'style-hierarchy' or empty($params?group))
                then attribute selected { 'true' } else () }style hierarchy</option>
              <option value="content-hierarchy">{ 
                if ($params?group = 'content-hierarchy')
                then attribute selected { 'true' } else () }content hierarchy</option>
            </select>
            <span> </span>
            {
              if ($svnurl and not($svnurl = $control:svnurlhierarchy)) then ( 
                <input id="cssa-search_restrict_path" name="restrict_path" type="checkbox" value="true">
                  {if ($params?restrict_path) then attribute checked { 'true' } else ()}
                </input>,
                <label for="search_restrict_path">restrict to { $svnurl => control-util:get-canonical-path() }</label>
              )
              else ()
            }
            {
              if ($svnurl) then <input type="hidden" name="svnurl" value="{$svnurl}"/> else ()
            }
             <input type="submit" value="Search styles"/>
          </div>
        </div>
      </form>
      <details class="search-hints">
        <summary>Search hints</summary>
        <h4>Caution</h4>
        <p>
          Unspecified searches (that is, from the top of the content hierarchy or without “name contains” terms)
          may take very long and may lead to a timeout. In this case please try to navigate to a content subtree first,
          give at least some style name substrings or limit the search to a single style type.
        </p>
        <h4> Name contains </h4>
        <p>
          You can enter space-separated tokens such as <code> text split </code>. Then all styles
          of the selected style type will be output whose name contains both <code> text </code> and
          <code> split </code>. The search is case insensitive, so for the given search, <code> p_text~box2~SPLIT </code>
          might be a result
        </p>
        <h4> Group by </h4>
        <p>
          Group by <code> style-hierarchy </code> groups all occurring styles by their InDesign
          style path component. Tilde additions will be ignored for grouping purposes. 
          When you arrive at the end of this style hierarchy, you can navigate the content
          hierarchy of the works where the given style occurs.
        </p>
      </details>
    </details>
    { $results?cssa }
  </div>
};
