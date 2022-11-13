<?xml version="1.0" encoding="UTF-8"?>
<p:declare-step xmlns:p="http://www.w3.org/ns/xproc"
                xmlns:c="http://www.w3.org/ns/xproc-step"
                xmlns:tr="http://transpect.io"
                version="1.0"
                type="tr:markdown2hub"
                name="markdown2hub">
  
  <p:documentation>
    This step converts a Markdown file to Hub. The href option
    expects an URI reference to the Markdown file.
  </p:documentation>
  
  <p:output port="result" />
  
  <p:option name="href">
    <p:documentation> URI reference to the MarkDown file </p:documentation>
  </p:option>
  
  <p:option name="debug" select="'yes'">
    <p:documentation>
      Used to switch debug mode on or off. Pass 'yes' to enable debug mode.
    </p:documentation>
  </p:option> 
  
  <p:option name="debug-dir-uri" select="'debug'">
    <p:documentation>
      Expects a file URI of the directory that should be used to store debug information. 
    </p:documentation>
  </p:option>
  
  <p:import href="http://transpect.io/xproc-util/file-uri/xpl/file-uri.xpl" />
  <p:import href="http://transpect.io/xproc-util/store-debug/xpl/store-debug.xpl" />
  
  <tr:file-uri name="get-markdown-file-uri">
    <p:with-option name="filename" select="$href" />
  </tr:file-uri>
  
  <p:xslt name="markdown2hub-transform" template-name="main">
    <p:input port="stylesheet">
      <p:document href="../xsl/markdown2hub.xsl"/>
    </p:input>
    <p:input port="source">
      <p:empty/>
    </p:input>
    <p:with-param name="href" select="/c:result/@href"/>
  </p:xslt>
  
  <tr:store-debug name="markdown2hub-debug" pipeline-step="markdown2hub/markdown2hub">
    <p:with-option name="active" select="$debug"/>
    <p:with-option name="base-uri" select="$debug-dir-uri"/>
  </tr:store-debug>
  
</p:declare-step>
