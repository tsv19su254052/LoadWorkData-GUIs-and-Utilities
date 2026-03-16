USE AirLinesDBNew62
GO

-- В кавычках вставить содержимое схемы из файла *.xsd
CREATE XML SCHEMA COLLECTION SchemaHREFs AS '
<!-- Начало вставки сводной XSD-схемы -->

<!-- Вверху сводный перечень пространств имен, todo Дополнить шапку из сгенерированной XSD-схемы -->

<xsd:schema  xmlns:xsd="http://www.w3.org/2001/XMLSchema"
			xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:xdt="http://www.w3.org/2004/07/xpath-datatypes"
            xmlns:fn="http://www.w3.org/2004/07/xpath-functions"
			xmlns:xml="http://www.w3.org/XML/1998/namespace"

            xmlns:xi="http://www.w3.org/2001/xinclude"
			xmlns:xlink="http://www.w3.org/1999/xlink"

			elementFormDefault="qualified"
			attributeFormDefault="unqualified"
			targetNamespace="myOwnNS">

	<xsd:annotation>
		<xsd:documentation>
			==== Сводная схема по сайтам ====
		</xsd:documentation>
	</xsd:annotation>

	<!-- todo Уточнить элементы из сгенерированной схемы и вставить их сюда
		Начало вставки -->

	<!-- Объявляем пользовательский составной тип данных
	 todo: вставить его в пользовательское пространство имен "myOwnNS"-->
	<xsd:complexType name="myHREF">
		<xsd:simpleContent>
			<xsd:extension base="xsd:anyURI">
				<xsd:attribute name="site" type="xsd:string" use="required"/>
			</xsd:extension>
		</xsd:simpleContent>
	</xsd:complexType>
	
	<xsd:element name="AirLine_HREFs">
		<xsd:complexType>
			<xsd:sequence>
				<xsd:element name="hrefToWikiPedia" type="myHREF"/>
				<xsd:element name="hrefToSite" type="myHREF"/>
				<!--
				<xsd:element name="hrefToWikiPedia">
					<xsd:complexType>
						<xsd:simpleContent>
							<xsd:extension base="xsd:anyURI">
								<xsd:attribute name="site" type="xsd:string" use="required" />
							</xsd:extension>
						</xsd:simpleContent>
					</xsd:complexType>
				</xsd:element>
				<xsd:element name="hrefToSite">
					<xsd:complexType>
						<xsd:simpleContent>
							<xsd:extension base="xsd:anyURI">
								<xsd:attribute name="site" type="xsd:string" use="required" />
							</xsd:extension>
						</xsd:simpleContent>
					</xsd:complexType>
				</xsd:element>
				-->
			</xsd:sequence>
		</xsd:complexType>
	</xsd:element>

	<!-- Окончание вставки
	todo: Сводную схему вставить в скрипт привязки, а лучше дать внутри скрипта привязки ссылку на этот файл схемы.
	-->

</xsd:schema>

<!-- Окончание вставки сводной XSD-схемы -->
<!-- todo Собранный перечень элементов вставить в скрипт привязки коллекции схем. Пропускать большие XML-ные файлы через большие и сложные схемы - не очень здорово, трудно искать несоответствия схеме -->
'

PRINT 'Привязал сводную XSD-схему к базе в коллекцию dbo.SchemaHREFs'
GO
