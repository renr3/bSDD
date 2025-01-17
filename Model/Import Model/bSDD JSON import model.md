# buildingSMART Data Dictionary model

The main concept of bSDD consists of a Domain having one or more Classifications and zero or more Properties. If we use IFC as an example, IFC is the Domain, "IfcWall" is a classification and "AcousticRating" is a Property. A Classification can have zero or more Properties. In the below scheme this is depicted as a database model.

<img src="https://github.com/buildingSMART/bSDD/blob/master/Model/Import%20Model/bSDD%20database%20diagram.png" alt="bSDD entity diagram"/>

# JSON import

You can deliver data for the buildingSMART Data Dictionary by using the bSDD
JSON import model format. This document explains this format.

Click on the link to get the list of allowed codes for [countries](https://api.bsdd.buildingsmart.org/api/Country/v1), [languages](https://api.bsdd.buildingsmart.org/api/Language/v1), [units](https://api.bsdd.buildingsmart.org/api/Unit/v1), [reference documents](https://api.bsdd.buildingsmart.org/api/ReferenceDocument/v1) and [ifc classification names](https://github.com/buildingSMART/bSDD/blob/master/Model/Import%20Model/reference-lists/ifc-classification-names.csv).
If you think there are reference items missing, please let us know.

## General notes

-- Default values will only be applied if a field is not specified. If you specify a field value of "null", the default will not be applied. Note that "null" may not be allowed for the field.

## Domain

Contains general information about the domain and the delivered data.

| Field            | DataType               | Required? | Translatable? | Description                                                                                                                                                                  |
|------------------|------------------------|-----------|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Classifications  | List of Classification | Yes       |               | List of objects of type “Classification”. See next section  |
| DomainCode       | Text                   | Yes       | No            | Code of the domain, preferably short, only alphabetical characters and numbes allowed, must start with alphabetical character E.g. “ifc”   |
| DomainName       | Text                   | If new domain or version | No  | Name of the domain. If the domain exists supplying this name is not necessary |
| DomainNamespaceUri      | Text                   | No        | No      | Required if UseOwnUri = true. Supply the globally unique namespace that's the first part of all Classifications and Properties namespaces, e.g. "urn:mycompany:mydomain" |
| DomainVersion    | Text                   | Yes       | No            | Version of the domain data in format "x.y". E.g.: 4.3 |
| LanguageIsoCode  | Text                   | Yes       | No            | ISO language code: indicates the language of the data. If you want to deliver data in multiple language use a json file per language. See reference list [languages](https://api.bsdd.buildingsmart.org/api/Language/v1). \* E.g. “de-DE” |
| LanguageOnly     | Boolean                | Yes       | No            | true if json contains only language specific information, no otherwise \*  |
| License          | Text                   | No        | No            | Description of the license the data will be made available (free text). E.g. “No license”, "MIT license"  |
| LicenseUrl      | Text                   | No        | No            | Url to a web page with the full license text   |
| MoreInfoUrl      | Text                   | No        | No            | Url to web page with more info about the domain |
| OrganizationCode | Text                   | Yes       | No            | If you do not have a code for your organization yet, request one at bsdd_support@buildingsmart.org                                                                                         |
| Properties       | List of Property       | Yes       |               | List of objects of type “Property”. See next sections |
| QualityAssuranceProcedure          | Text                   | No        | No            | Name or short description of the quality assurance procedure used for the domain, e.g. "ETIM international", "-	AFNOR NF XP P07-150 (PPBIM)", "bSI process", "UN GHS 2015", "UN CPC 1.1", "Private", "Unknown" |
| QualityAssuranceProcedureUrl      | Text                   | No        | No            | Url to a web page with more detailed info on the quality assurance procedure, e.g. "https://www.buildingsmart.org/about/bsi-process"  |
| ReleaseDate      | Date                   | No        | No            | Date of release of the version E.g. “2017-10-01”  |
| Status      | Text                   | No        | No            | State of this version. Must be one of: "Preview", "Active", "Inactive"  |
| UseOwnUri      | Boolean                   | No        | No            | Use your own namespace uri for global unique identification of Classifications and Properties. If you don't use your own namespace URI a namespace URI starting with "http://bsdd.buildingsmart.org" will be assigned to each Classification and Property |

\* For delivering data in additional languages it is sufficient to fill the Domain type fields, all “Code” fields and the fields marked with “Translatable? = Yes” of the other types. Make sure that the OrganizationCode, DomainCode and DomainVersion are exactly the same and if the data is for adding a language to an existing Domain, set field “LanguageOnly” to true.

## Classification

A classification can be any (abstract) object (e.g. “IfcWall”), abstract concept
(e.g. “Costing”) or process (e.g. “Installation”). Classifications can be
organized in a tree like structure. For example: “IfcCurtainWall” is a more
specific classification of “IfcWall”. We use the term “parent” to identify this
relation: the parent of “IfcCurtainWall” is “IfcWall”.

| Field                     | DataType                       | Required? | Translatable? | Description                                                                                                        |
|---------------------------|--------------------------------|-----------|---------------|--------------------------------------------------------------------------------------------------------------------|
| ActivationDateUtc         | Date                           | No        | No            | Will get date of import if field not present |
| ClassificationProperties  | List of ClassificationProperty | No        | No            | See next sections |
| ClassificationRelations   | List of ClassificationRelation | No        | No            | See next sections |
| ClassificationType        | Text                           | No        | No            | Must be one of: Class ComposedProperty Domain ReferenceDocument AlternativeUse                                     |
| Code                      | Text                           | Yes       | No            | Unique identification within the domain of the classification E.g. “ifc-00123-01”                                  |
| ReferenceCode             | Text                           | No        | No            | Reference code, can have domain specific usage. If null, then the value of Code is used to fill the field. To make ReferenceCode empty use empty string "".  |
| CountriesOfUse            | List of text                   | No        | No            | List of country ISO codes this Classification is being used. See reference list [countries](https://api.bsdd.buildingsmart.org//api/Country/v1).                                    |
| CountryOfOrigin           | Text                           | No        | No            | ISO Country Code of the country of origin of this classification. See reference list [countries](https://api.bsdd.buildingsmart.org//api/Country/v1).                                         |
| CreatorLanguageIsoCode    | Text                           | No        | No            | Language ISO code of the creator. See reference list [languages](https://api.bsdd.buildingsmart.org/api/Language/v1). |
| DeactivationDateUtc       | Date                           | No        | No            | |
| Definition                | Text                           | No        | Yes           | Definition of the Classification                                                                                   |
| DeprecationExplanation    | Text                           | No        | Yes           |  |
| DocumentReference         | Text                           | No        | No            | Reference to document with full or official definition of the Classification. See reference list [reference documents](https://api.bsdd.buildingsmart.org/api/ReferenceDocument/v1). |
| Name                      | Text                           | Yes       | Yes           | Name of the classification E.g. “IfcCurtainWall”                                                                   |
| OwnedUri                | Text                           | No        | No           | If you specified "UseOwnUri = true" at domain level you must supply the namepsace URI that globally uniquely identifies the Classifciation  |
| ParentClassificationCode  | Text                           | No        | No            | Reference to the parent Classification. The ID in this field MUST exist in the data delivered. E.g. “ifc-00123-00” |
| RelatedIfcEntityNamesList | List of text                   | No        | No            | References to the IFC equivalent of this Classification. See reference list [ifc classification names](https://github.com/buildingSMART/bSDD/blob/master/Model/Import%20Model/reference-lists/ifc-classification-names.csv).                                      |
| ReplacedObjectCodes       | List of text                   | No        | No            | List of Classification Codes this Classification replaces                                                          |
| ReplacingObjectCodes      | List of text                   | No        | No            | List of Classification Codes this classification is replaced by                                                    |
| RevisionDateUtc           | Date                           | No        | No            |  |
| RevisionNumber            | Integer                        | No        | No            |  |
| Status                    | Text                           | No        | No            | Status of the Classification: “Active” (default) or “Inactive” |
| SubdivisionsOfUse         | List of text                   | No        | Yes           | List of geographical regions of use E.g. “US-MT”  |
| Synonyms                  | List of text                   | No        | Yes           | |
| VersionDateUtc            | Date                           | No        | No            | Will get date of import if field not present |
| VersionNumber             | Integer                        | No        | No            |  |
| VisualRepresentationUri   | Text                           | No        | Yes           |  |


## Material

A material is similar to a classification.
Differences in model are:
- no ClassificationType field
- "ParentMaterialCode" instead of "ParentClassificationCode"
- "MaterialProperties" instead of "ClassificationProperties"

A domain can have both Materials and Classifications. Please note that the "code" of both Materials and Classifications must be unique within the domain. You can't have a domain with Material with code "abcd" and a Classification with the same code "abcd".

## Property

A classification can have multiple properties and a property can be part of many
classifications

| Field                         | DataType     | Required? | Translatable? | Description                                                                                                                                          |
|-------------------------------|--------------|-----------|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| ActivationDateUtc             | Date         | No        | No            | Will get date of import if field not present |
| AllowedValues              | List of PropertyValue  | No  | Yes           | List of allowed values for the property. Note: do not use this one for properties of type boolean. See section "PropertyValue type" for more info |
| Code                          | Text         | Yes       | No            | Unique identification within the domain of the property E.g. “ifc-99088-01”                                                                          |
| ConnectedPropertyCodes        | List of text | No        | No            | List of codes of connected properties                                                                                                                |
| CountriesOfUse                | Text         | No        | No            | Semicolon separated list of country ISO codes this Classification is being used. See reference list (json) [countries](https://api.bsdd.buildingsmart.org/api/Country/v1).                                                      |
| CountryOfOrigin               | Text         | No        | No            | ISO Country Code of the country of origin of this classification. See reference list.                                                                           |
| CreatorLanguageIsoCode        | Text         | No        | No            | Language ISO code of the creator. See reference list (json)[languages](https://api.bsdd.buildingsmart.org/api/Language/v1)  |
| DataType                      | Text         | No        | No            | The datatype the property is expressed in. Must be one of:  Boolean,  Character,  Integer,  Real,  String,  Time                       |
| DeactivationDateUtc           | Date         | No        | No            |  |
| Definition                    | Text         | No        | Yes           | Definition of the Property |
| DeprecationExplanation        | Text         | No        | Yes           |  |
| Description                   | Text         | Yes       | Yes           | |
| Dimension                     | Text         | No        | No            | In case of a physical quantity, dimension according to ISO 80000 (all parts) E.g. “1 0 -2 0 0 0 0”                                                   |
| DimensionLength               | Integer      | No        | No            | The Length dimension; either use the field Dimension to specifiy all parts, or specify all parts separately|
| DimensionMass               | Integer      | No        | No            | The Mass dimension; either use the field Dimension to specifiy all parts, or specify all parts separately|
| DimensionTime               | Integer      | No        | No            | The Time dimension; either use the field Dimension to specifiy all parts, or specify all parts separately|
| DimensionElectricCurrent               | Integer      | No        | No            | The ElectricCurrent dimension; either use the field Dimension to specifiy all parts, or specify all parts separately|
| DimensionThermodynamicTemperature               | Integer      | No        | No            | The ThermodynamicTemperature dimension; either use the field Dimension to specifiy all parts, or specify all parts separately|
| DimensionAmountOfSubstance               | Integer      | No        | No            | The AmountOfSubstance dimension; either use the field Dimension to specifiy all parts, or specify all parts separately|
| DimensionLuminousInensity               | Integer      | No        | No            | The LuminousInensity dimension; either use the field Dimension to specifiy all parts, or specify all parts separately|
| DocumentReference             | Text         | No        | No            | Reference to document with full or official definition of the Property. See reference list (json) [reference documents](https://api.bsdd.buildingsmart.org/api/ReferenceDocument/v1).                                                                               |
| DynamicParameterPropertyCodes | List of text | No        | No            | List of codes of properties which are parameters of the function for a dynamic property                                                              |
| Example                       | Text         | No        | Yes           | Example of the Property |
| IsDynamic                     | Boolean      | No        | No            | Default: false If this is a dynamic property, the value is dependent on the parameters provided in field DynamicParameterProperties                  |
| MaxExclusive            | Real     | No        | No            | Maximum allowed value, exclusive - do not fill both 'inclusive' and 'exclusive' values |
| MaxInclusive            | Real     | No        | No            | Maximum allowed value, inclusive - do not fill both 'inclusive' and 'exclusive' values |
| MinExclusive            | Real     | No        | No            | Minimum allowed value, exclusive |
| MinInclusive            | Real     | No        | No            | Minimum allowed value, inclusive |
| MethodOfMeasurement           | Text         | No        | Yes           | E.g. “Thermal transmittance according to ISO 10077-1”                                                                                                |
| Name                          | Text         | Yes       | Yes           | Name of the Property E.g. “IsExternal”                                                                                                               |
| OwnedUri                | Text                           | No        | No           | If you specified "UseOwnUri = true" at domain level you must supply the namepsace URI that globally uniquely identifies the Property  |
| Pattern            | Text     | No        | No            | An [XML Schema regular expression](https://www.regular-expressions.info/xml.html) to limit allowed values |
| PhysicalQuantity              | Text         | No        | Yes           | Name of the physical quantity of the property E.g. “without” or “mass”                                                                               |
| PropertyValueKind             | Text         | No        | No            | Must be one of:  Single (one value, is default),  Range (two values),  List (multiple values), Complex (consists of multiple properties, use ConnectedProperties), ComplexList (list of complex values)                       |
| ReplacedObjectCodes           | List of text | No        | No            | List of Classification Codes this Classification replaces                                                                                            |
| ReplacingObjectCodes          | List of text | No        | No            | List of Classification Codes this classification is replaced by                                                                                      |
| RevisionDateUtc               | Date         | No        | No            |  |
| RevisionNumber                | Integer      | No        | No     |  |
| Status                        | Text         | No        | No            | Status of the Property: “Active” (default) or “Inactive”    |
| SubdivisionsOfUse             | Text         | No        | Yes           | Semicolon separated list of geographical regions of use E.g. “US-MT”                                                                                 |
| TextFormat                    | Text         | No        | No            | Pair for text type (encoding, number of characters) The encoding is set according to “Name of encoding standard” of IANA, RFC 2978 E.g. “(UTF-8,32)” |
| Units                         | List of text | No        | No            | The units to represent a scale that enables a value to be measured (ISO 80000 or ISO 4217 or ISO 8601). List of values. See reference list (json) [units](https://api.bsdd.buildingsmart.org/api/Unit/v1).  We are working on supporting the [QUDT](http://www.qudt.org/) vocabulary. If you would like to import using QUDT units or want to have the QUDT units in the API output pls let us know. |
| VersionDateUtc                | Date         | No        | No            | Will get date of import if field not present |
| VersionNumber                 | Integer      | No        | No            |  |
| VisualRepresentationUri       | Text         | No        | Yes           |  |
| PropertyRelations              | List of PropertyRelation  | No  | Yes           | List of related properties. See section "PropertyRelation type" for more info |


## ClassificationProperty type

| Field               | DataType | Required? | Translatable? | Description                                                                                                            |
|---------------------|----------|-----------|---------------|------------------------------------------------------------------------------------------------------------------------|
| AllowedValues              | List of PropertyValue  | No  | Yes           | List of allowed values for the property. Do not use this one for properties of type boolean. See section "PropertyValue type" for more info |
| Code                | Text     | No        | No            | Unique identification within the domain of this classification property                                                |
| Description         | Text     | No        | Yes           | You can supply the property description specific for the classification. If left out, the 'common' description of the property will be shown where applicable |
| ExternalPropertyUri | Text     | No \*     | No            | Reference to the property if it is in a different domain, preferably using a bSDD namespace uri, e.g. http://identifier.buildingsmart.org/uri/buildingsmart/ifc-4.3/prop/position                                                                       |
| IsRequired              | Boolean  | No  | Yes           | Indicates if this is a required property of the classification |
| IsWritable              | Boolean  | No  | Yes           | Indicates if the value of this property of the classification can be changed |
| MaxExclusive            | Real     | No        | No            | Maximum allowed value, exclusive. Overrides the value defined for the Property. Do not fill both 'inclusive' and 'exclusive' values |
| MaxInclusive            | Real     | No        | No            | Maximum allowed value, inclusive. Overrides the value defined for the Property. Do not fill both 'inclusive' and 'exclusive' values. |
| MinExclusive            | Real     | No        | No            | Minimum allowed value, exclusive. Overrides the value defined for the Property |
| MinInclusive            | Real     | No        | No            | Minimum allowed value, inclusive. Overrides the value defined for the Property |
| Pattern            | Text     | No        | No            | An [XML Schema regular expression](https://www.regular-expressions.info/xml.html) to limit allowed values. Overrides the pattern defined for the Property |
| PredefinedValue     | Text     | No        | No            | Predefined value for this property. E.g. value for property “IsLoadBearing” can be “true” for classification “IfcWall” |
| PropertyCode        | Text     | No \*     | No            | Reference to the property if it is in the same domain. You can leave this one empty if you fill the ExternalPropertyUri  |
| PropertySet         | Text     | No        | No            | Name of the property set in which the property should be placed during IFC export. When the property should be placed in an IFC entity you should use that. For example when you property is a material you should use the value "IfcMaterial".                                                                                                                    |
| PropertyType        | Text     | No        | No            | Type of the Property for the classification: “Property” (default) or “Dependency”                                      |
| SortNumber          | Integer  | No        | No            | Sort number of this property within the classification                                                                 |
| Symbol              | Text     | No        | No            |                                                                                                                        |
| Unit                | Text     | No        | No            | See reference list (json) [units](https://api.bsdd.buildingsmart.org/api/Unit/v1).                                                                                                                       |

\* One of those is required.

## ClassificationRelation type

| Field                    | DataType | Required? | Translatable? | Description                                                                 |
|--------------------------|----------|-----------|---------------|-----------------------------------------------------------------------------|
| RelatedClassificationUri | Text     | Yes       | No            | Full namespace URI of the related classification. Can be to same or different domain. Example: http://identifier.buildingsmart.org/uri/etim/etim-8.0/class/EC002987|
| RelationType             | Text     | Yes       | No            | One of:  HasMaterial, HasReference,  IsEqualTo,  IsSynonymOf,  IsParentOf,  IsChildOf, HasPart    |

## PropertyValue type

Note: adding translations of the PropertyValue is not supported yet

| Field                    | DataType | Required? | Translatable? | Description                                                                 |
|--------------------------|----------|-----------|---------------|-----------------------------------------------------------------------------|
| Code             | Text     | No       | No            | Code as unique identification of the value (max 20 characters). If you want to add translations of Values or their Descriptions, you must supply a Code for each Value    |
| Description | Text     | No       | Yes            | A description of the value|
| NamespaceUri| Text | No | No | You can provide your own Namespace Uri (must be globally unique).|
| SortNumber | Integer     | No       | No            | SortNumber of the Value in the list of Values of the Property it belongs to|
| Value | Text     | Yes       | Yes            | One of the Values the property can have, e.g. "Green" in case the Property is something like "Color"|

## PropertyRelation type

| Field                    | DataType | Required? | Translatable? | Description                                                                 |
|--------------------------|----------|-----------|---------------|-----------------------------------------------------------------------------|
| RelatedPropertyUri | Text     | Yes       | No            | Full namespace URI of the related property. Can be to same or different domain.|
| RelationType             | Text     | Yes       | No            | One of:  HasReference,  IsEqualTo,  IsSynonymOf,  IsParentOf,  IsChildOf, HasPart    |
