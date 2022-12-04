import module namespace svn             = 'io.transpect.basex.extensions.subversion.XSvnApi';
import module namespace control         = 'http://transpect.io/control' at '../control/control.xq';
import module namespace control-i18n    = 'http://transpect.io/control/util/control-i18n' at '../control/util/control-i18n.xq';
import module namespace control-util    = 'http://transpect.io/control/util/control-util' at '../control/util/control-util.xq';
import module namespace control-widgets = 'http://transpect.io/control/util/control-widgets' at '../control/util/control-widgets.xq';
import module namespace control-backend = 'http://transpect.io/control-backend' at '../control-backend/control-backend.xqm';


declare
  %updating
function control-backend:fill-content-index-dbs2($customization as xs:string, $wcpath as xs:string?) {
    (: the fulltext and content dbs must exist before invoking this, as well as a populated INDEX db :)
    let $index := db:open('INDEX', 'index.xml'),
        $hierarchy-repo := $control:config/control:repos/control:repo[@role = 'hierarchy'],
        $hierarchy-path := $hierarchy-repo/@path,
        $content-paths := for $pattern in ($control:config/control:ftindexes/control:file/@pattern,
                                           $control:config/control:also-indexable/control:file/@pattern)
                          return $index//file/@virtual-path[matches(., $pattern)]
    return
      for $cp in $content-paths
      let $wcp := replace($cp, '^' || $hierarchy-path, $wcpath),
          $dbp := $cp/../@svnpath => control-util:get-local-path()
      return control-backend:add-xml-by-path($wcp, $dbp, $customization)
};

control-backend:fill-content-index-dbs2('default', $control:config/control:repos/control:repo[@role = 'hierarchy']/@wc-path)
