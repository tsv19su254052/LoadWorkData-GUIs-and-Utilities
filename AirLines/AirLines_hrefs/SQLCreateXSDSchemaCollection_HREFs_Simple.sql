USE AirLinesDBNew62
GO

-- В кавычках вставить содержимое схемы из файла *.xsd
CREATE XML SCHEMA COLLECTION SchemaHREFs AS '
<!-- Начало вставки сводной XSD-схемы -->

<!-- Вверху сводный перечень пространств имен, todo Дополнить шапку из сгенерированной XSD-схемы -->

<xsd:schema  xmlns:xsd="http://www.w3.org/2001/XMLSchema"
			attributeFormDefault="unqualified"
			elementFormDefault="qualified"
			targetNamespace="myNS">

	<xsd:annotation>
		<xsd:documentation>
			==== Сводная схема по сайтам ====
		</xsd:documentation>
	</xsd:annotation>

	<!-- todo Вставить элементы из сгенерированных XSD-схем -->
	<!-- Начало вставки -->

	<xsd:element name="AirLine_HREFs">
		<xsd:complexType>
			<xsd:sequence>
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
			</xsd:sequence>
		</xsd:complexType>
	</xsd:element>

	<!-- Окончание вставки -->

</xsd:schema>

<!-- Окончание вставки сводной XSD-схемы -->
<!-- todo Собранный перечень элементов вставить в скрипт привязки коллекции схем. Пропускать большие XML-ные файлы через большие и сложные схемы - не очень здорово, трудно искать несоответствия схеме -->
'

PRINT 'Привязал сводную XSD-схему к базе в коллекцию dbo.SchemaHREFs'
GO
