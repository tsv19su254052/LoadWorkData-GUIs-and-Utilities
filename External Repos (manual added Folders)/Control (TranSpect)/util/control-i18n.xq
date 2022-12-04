module namespace control-i18n = 'http://transpect.io/control/util/control-i18n';

(: 
 : prints the parent directory of a path , 
 : e.g. /home/parentdir/mydir/ => /home/parentdir/ 
 :)
declare function control-i18n:localize( $name as xs:string, $locale as xs:string ) as xs:string{
  for $locale in doc('../i18n/i18n.xml')/i18n/entry[@name eq $name]/locale[@lang eq $locale]
  return $locale
};
