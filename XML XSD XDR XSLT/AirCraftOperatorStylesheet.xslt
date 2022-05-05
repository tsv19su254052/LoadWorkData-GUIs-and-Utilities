<?xml version="1.0" encoding="UTF-8" ?>

<xsl:stylesheet version="1.0"
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        xmlns="http://www.w3.org/1999/xhtml">
	<xsl:output method="xml" indent="yes"
        doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
        doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"/>

	<!--XHTML document outline-->
	<xsl:template match="/">
		<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
			<head>
				<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
				<title>test1</title>
				<style type="text/css">
					h1          { padding: 10px; padding-width: 100%; background-color: silver }
					td, th      { width: 40%; border: 1px solid silver; padding: 10px }
					td:first-child, th:first-child  { width: 20% }
					table       { width: 650px }
				</style>
			</head>
			<body>
				<xsl:apply-templates/>
			</body>
		</html>
	</xsl:template>

	<!--Table headers and outline-->
	<xsl:template match="domains/*">
		<h1>
			<xsl:value-of select="@ownedBy"/>
		</h1>
		<p>
			The following host names are currently in use at
			<strong>
				<xsl:value-of select="local-name(.)"/>
			</strong>
		</p>
		<table>
			<tr>
				<th>Host name</th>
				<th>URL</th>
				<th>Used by</th>
			</tr>
			<xsl:apply-templates/>
		</table>
	</xsl:template>

	<!--Table row and first two columns-->
	<xsl:template match="host">
		<!--Create variable for 'url', as it's used twice-->
		<xsl:variable name="url" select=
            "normalize-space(concat('http://', normalize-space(node()), '.', local-name(..)))"/>
		<tr>
			<td>
				<xsl:value-of select="node()"/>
			</td>
			<td>
				<a href="{$url}">
					<xsl:value-of select="$url"/>
				</a>
			</td>
			<xsl:apply-templates select="use"/>
		</tr>
	</xsl:template>

	<!--'Used by' column-->
	<xsl:template match="use">
		<td>
			<xsl:value-of select="."/>
		</td>
	</xsl:template>

</xsl:stylesheet>