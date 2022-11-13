<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:xs="http://www.w3.org/2001/XMLSchema"
                xmlns:md="https://commonmark.org"
                xmlns:tr="http://transpect.io"
                xmlns="http://docbook.org/ns/docbook"
                xpath-default-namespace="http://docbook.org/ns/docbook"
                exclude-result-prefixes="xs md tr"
                version="2.0">
  
  <!-- *
       * converts Markdown to Hub XML.
       *
       * usage: either call md:transform($markdown) 
       *        from an importing stylesheet or invoke 
       *        the initial template:
       *        
       *        $ saxon -xsl saxon -xsl:xsl/markdown2hub.xsl \
       *        -it:main href=file:/markdown2hub/README.md -o:out.hub.xml
       * -->
  
  <!-- href expects an file uri -->
  
  <xsl:param name="href" as="xs:string"/>
  
  <!-- *
       * global variables
       * -->

  <xsl:variable name="markdown"                      as="xs:string" select="unparsed-text($href)"/>
  <xsl:variable name="md:table-horizontal-sep-regex" as="xs:string" select="'---+\s*\|'"/>
  <xsl:variable name="md:table-vertical-sep-regex"   as="xs:string" select="'\|'"/>
  <xsl:variable name="md:list-marker-regex"          as="xs:string" select="'((([-\*]+|[\d]\.?))+)'"/>
  <xsl:variable name="md:codeblock-regex"            as="xs:string" select="'^\s*```([a-z]+)?'"/>
  <xsl:variable name="md:blockquote-regex"           as="xs:string" select="'^\s*&gt;'"/>
  <xsl:variable name="md:bold-italic-regex"          as="xs:string" select="'[\*_]{1,2}.+[\*_]{1,2}'"/>
  <xsl:variable name="md:image-regex"                as="xs:string" select="'!\[(.+?)\]\((.+?)\)'"/>
  <xsl:variable name="md:hyperlinks-regex"           as="xs:string" select="'\[(.+?)\]\((.+?)\)'"/>
  
  <!-- *
       * initial template
       * -->
  
  <xsl:template name="main">
    <xsl:sequence select="md:transform($markdown)"/>
  </xsl:template>
  
  <!-- *
       * identity template
       * -->
  
  <xsl:template match="@*|*" mode="#all">
    <xsl:copy>
      <xsl:apply-templates select="@*, node()" mode="#current"/>
    </xsl:copy>
  </xsl:template>
  
  <!-- *
       * mode md:transform
       * -->
  
  <xsl:template match="orderedlist/para
                      |itemizedlist/para" mode="md:transform">
    <listitem override="{replace(., concat('\s*', $md:list-marker-regex, '.+?$'), '$1')}">
      <para>
        <xsl:value-of select="normalize-space(replace(., $md:list-marker-regex, ''))"/>
      </para>
    </listitem>
  </xsl:template>
  
  <xsl:template match="programlisting" mode="md:transform">
    <xsl:variable name="code-lang" as="xs:string"
                  select="preceding-sibling::*[1][matches(., $md:codeblock-regex)]/replace(., $md:codeblock-regex, '$1')"/>
    <xsl:copy>
      <xsl:if test="normalize-space($code-lang)">
        <xsl:attribute name="role" select="$code-lang"/>
      </xsl:if>
      <xsl:apply-templates mode="#current"/>
    </xsl:copy>
  </xsl:template>
  
  <xsl:template match="programlisting/para" mode="md:transform">
    <xsl:apply-templates mode="#current"/>
    <xsl:if test="position() ne last()">
      <xsl:text>&#xa;</xsl:text>
    </xsl:if>
  </xsl:template>
  
  <xsl:template match="para[not(normalize-space())]" mode="md:transform"/>
  
  <xsl:template match="text()" mode="md:transform">
    <xsl:apply-templates select="md:bold-italics(.)" mode="md:images"/>
  </xsl:template>
  
  <xsl:template match="para[matches(., $md:codeblock-regex)][normalize-space()]" mode="md:transform"/>
  
  <!-- *
       * mode md:images
       * -->
  
  <xsl:template match="text()" mode="md:images">
    <xsl:apply-templates select="md:images(.)" mode="md:hyperlinks"/>
  </xsl:template>
  
  <!-- *
       * mode md:hyperlinks
       * -->
  
  <xsl:template match="text()" mode="md:hyperlinks">
    <xsl:sequence select="md:hyperlinks(.)"/>
  </xsl:template>
  
  <!-- *
       * mode md:blockquotes
       * -->
  
  <xsl:template match="para" mode="md:blockquotes">
    <xsl:copy>
      <xsl:value-of select="replace(., '^\s*&gt;\s*', '')"/>
    </xsl:copy>
  </xsl:template>
  
  <!-- *
       * mode md:tables
       * -->
  
  <xsl:template match="para[matches(., $md:table-horizontal-sep-regex)]" mode="md:tables"/>
  
  <xsl:template match="para" mode="md:tables">
    <xsl:variable name="is-th" as="xs:boolean" 
                  select="exists(following-sibling::*[1][matches(., $md:table-horizontal-sep-regex)])"/>
    <tr>
      <xsl:for-each select="tokenize(., '[\d\s\w]\|')">
        <xsl:element name="{('th'[$is-th], 'td')[1]}">
          <xsl:sequence select="normalize-space(.)"/>
        </xsl:element>
      </xsl:for-each>
    </tr>
  </xsl:template>
  
  <!-- *
       * mode md:sections
       * -->
  
  <xsl:template match="para" mode="md:sections">
    <title>
      <xsl:value-of select="replace(., '^#+\s*', '')"/>
    </title>
  </xsl:template>
  
  <!-- *
       * functions
       * -->
  
  <xsl:function name="md:transform" as="element(hub)">
    <xsl:param name="markdown" as="xs:string"/>
    <hub>
      <info>
        <title><xsl:value-of select="replace($href, '^(.+/)(.+)?$', '$2')"/></title>
      </info>
      <xsl:apply-templates select="md:sectionize(
                                       md:create-lists(
                                           md:create-quotes(
                                               md:create-tables(
                                                   md:create-blocks(
                                                       md:split-lines($markdown)
                                                   )
                                               )
                                           ), 0
                                       ), 0
                                   )" 
                           mode="md:transform"/>
    </hub>
  </xsl:function>
  
  <xsl:function name="md:images">
    <xsl:param name="str"/>
    <xsl:analyze-string select="$str" regex="{$md:image-regex}">
      <xsl:matching-substring>
        <mediaobject>
          <imageobject>
            <imagedata fileref="{regex-group(2)}"/>
          </imageobject>
          <xsl:if test="regex-group(1)">
            <caption>  
              <xsl:value-of select="regex-group(1)"/>
            </caption>
          </xsl:if>
        </mediaobject>
      </xsl:matching-substring>
      <xsl:non-matching-substring>
        <xsl:value-of select="."/>
      </xsl:non-matching-substring>
    </xsl:analyze-string>
  </xsl:function>
  
  <xsl:function name="md:hyperlinks">
    <xsl:param name="str"/>
    <xsl:analyze-string select="$str" regex="{$md:hyperlinks-regex}">
      <xsl:matching-substring>
        <link xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="{regex-group(2)}">
          <xsl:value-of select="regex-group(1)"/>
        </link>
      </xsl:matching-substring>
      <xsl:non-matching-substring>
        <xsl:value-of select="."/>
      </xsl:non-matching-substring>
    </xsl:analyze-string>
  </xsl:function>
  
  <xsl:function name="md:bold-italics">
    <xsl:param name="str"/>
    <xsl:analyze-string select="$str" regex="{$md:bold-italic-regex}">
      <xsl:matching-substring>
        <xsl:variable name="style" select="if(matches(., '[\*_]{2}')) then 'bold' else 'italics'"/>
        <emphasis>
          <xsl:attribute name="role" select="$style"/>
          <xsl:value-of select="replace(., '[\*_]+', '')"/>  
        </emphasis>
      </xsl:matching-substring>
      <xsl:non-matching-substring>
        <xsl:value-of select="."/>
      </xsl:non-matching-substring>
    </xsl:analyze-string>
  </xsl:function>
  
  <xsl:function name="md:create-quotes" as="element()*">
    <xsl:param name="blocks" as="element()*"/>
    <xsl:for-each-group select="$blocks"
                        group-adjacent="matches(., $md:blockquote-regex)">
      <xsl:choose>
        <xsl:when test="current-grouping-key()">
          <blockquote>
            <xsl:apply-templates select="current-group()" mode="md:blockquotes"/>
          </blockquote>
        </xsl:when>
        <xsl:otherwise>
          <xsl:sequence select="current-group()"/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each-group>
  </xsl:function>
  
  <xsl:function name="md:create-lists" as="element()*">
    <xsl:param name="blocks" as="element()*"/>
    <xsl:param name="level" as="xs:integer"/>
    <xsl:variable name="marker-regex" as="xs:string" 
                  select="string-join(('^\s*(',
                                       for $i in (0 to $level) return '[-\*]',
                                       '|',
                                       for $i in (0 to $level) return '[\d+][\.\)]',
                                       '\s*)'), 
                                      '')"/>
    <xsl:for-each-group select="$blocks"
                        group-adjacent="matches(., $marker-regex)">
      <xsl:choose>
        <xsl:when test="current-grouping-key()">
          <xsl:choose>
            <xsl:when test="matches(normalize-space(current-group()[1]), '^---+$') and count(current-group()) eq 1">
              <bridgehead role="separator"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:element name="{if(matches(current-group()[1], '^\d+')) 
                                  then 'orderedlist' 
                                  else 'itemizedlist'}">
                <xsl:choose>
                  <xsl:when test="some $listitem in current-group() 
                                  satisfies matches($listitem, string-join(('^(',
                                                                     for $listitem in (0 to $level + 1) return '[\*\-]',
                                                                     '|',
                                                                     for $listitem in (0 to $level + 1) return '\d+[\.\)]',
                                                                     '\s*)'), 
                                                                    ''))">
                    <xsl:sequence select="md:create-lists(current-group(), $level + 1)"/>
                  </xsl:when>
                  <xsl:otherwise>
                    <xsl:sequence select="current-group()"/>
                  </xsl:otherwise>
                </xsl:choose>
              </xsl:element>    
            </xsl:otherwise>
          </xsl:choose>
        </xsl:when>
        <xsl:otherwise>
          <xsl:sequence select="current-group()"/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each-group>
  </xsl:function>
  
  <xsl:function name="md:create-tables" as="element()*">
    <xsl:param name="blocks" as="element()*"/>
    <xsl:for-each-group select="$blocks" 
                        group-adjacent="(    self::*[1][matches(., $md:table-horizontal-sep-regex)]
                                         and following-sibling::*[1][matches(., $md:table-vertical-sep-regex)]
                                         )
                                        or 
                                        (    self::*[1][matches(., $md:table-vertical-sep-regex)]
                                         and (   preceding-sibling::*[matches(., $md:table-horizontal-sep-regex)]
                                              or following-sibling::*[1][matches(., $md:table-horizontal-sep-regex)]
                                              )
                                         )">
      <xsl:choose>
        <xsl:when test="current-grouping-key() eq true()">
          <table>
            <xsl:apply-templates select="current-group()" mode="md:tables"/>
          </table>
        </xsl:when>
        <xsl:otherwise>
          <xsl:sequence select="current-group()"/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each-group>
  </xsl:function>  
  
  <xsl:function name="md:create-blocks" as="element()*">
    <xsl:param name="hub" as="element(hub)"/>
    <xsl:for-each-group select="$hub/*" 
                        group-adjacent="    count(preceding-sibling::para[matches(., $md:codeblock-regex)]) mod 2 eq 1
                                        and count(following-sibling::para[matches(., $md:codeblock-regex)]) mod 2 eq 1">
      <xsl:choose>
        <xsl:when test="current-grouping-key() eq true()">
          <programlisting>
            <xsl:sequence select="current-group()"/>
          </programlisting>
        </xsl:when>
        <xsl:otherwise>
          <xsl:sequence select="current-group()"/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each-group>
  </xsl:function>
  
  <xsl:function name="md:sectionize" as="element()*">
    <xsl:param name="blocks" as="element()*"/>
    <xsl:param name="level" as="xs:integer"/>
    <xsl:variable name="hashtag-regex" as="xs:string" 
                  select="string-join(('^', for $i in (0 to $level) return '#', '\s'), '')"/>
    <xsl:for-each-group select="$blocks" group-starting-with="self::para[matches(., $hashtag-regex)]">
      <xsl:choose>
        <xsl:when test="current-group()[self::para[matches(., $hashtag-regex)]]">
          <section role="sect-{$level + 1}">
            <xsl:apply-templates select="current-group()[1]" mode="md:sections"/>
            <xsl:sequence select="md:sectionize(current-group()[position() ne 1], $level + 1)"/>
          </section>
        </xsl:when>
        <xsl:otherwise>
          <xsl:sequence select="current-group()"/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each-group>
  </xsl:function>
  
  <xsl:function name="md:split-lines" as="element(hub)">
    <xsl:param name="str" as="xs:string"/>
    <xsl:variable name="lines" as="xs:string*" select="tokenize($str, '\n', 'm')"/>
    <hub>
      <xsl:for-each select="$lines">
        <para>
          <xsl:sequence select="."/>
        </para>
      </xsl:for-each>
    </hub>
  </xsl:function>
  
</xsl:stylesheet>