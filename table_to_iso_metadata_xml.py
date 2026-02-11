import pandas as pd
import json
import shutil
import sys
from datetime import datetime
import xml.etree.ElementTree as ET
import os

ns = {
    "gmd": "http://www.isotc211.org/2005/gmd",
    "gco": "http://www.isotc211.org/2005/gco",
    "gmx": "http://www.isotc211.org/2005/gmx",
    "gml": "http://www.opengis.net/gml"
}

platform_base_url = "https://exposome.uu.nl/"

def update_xml_from_row(row, xml_path):
    print(f"\n Updating {row['Title']}")


    tree = ET.parse(xml_path)
    root = tree.getroot()

    # ### Update abstract ###
    table_abstract = row['Summary']
    element_abstract = root.find('gmd:identificationInfo/gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString', namespaces=ns)

    if table_abstract != element_abstract.text:
        print(f"Updating summary/abstract to: {table_abstract}")
        element_abstract.text = table_abstract

    # ### Update Metadata last updated
    table_md_last_updated = datetime.strptime(row['Metadata last updated'], "%d-%m-%Y").date().isoformat() 

    element_md_last_updated = root.find('gmd:dateStamp/gco:Date', namespaces=ns)

    if table_md_last_updated != element_md_last_updated.text:
        print(f"Updating Metadata last updated to: {table_md_last_updated}")
        element_md_last_updated.text = table_md_last_updated

    ### Update Dataset last revised
    table_dataset_last_revised = datetime.strptime(row['Dataset last revised'], "%d-%m-%Y").date().isoformat() 
    element_dataset_last_revised = root.find('gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date/gco:Date', namespaces=ns)

    if table_dataset_last_revised != element_dataset_last_revised.text:
        print(f"Updating Dataset last revised to: {table_dataset_last_revised}")
        element_dataset_last_revised.text = table_dataset_last_revised

    # ### Update Title ###
    table_title = row['Title']
    element_title = root.find('gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString', namespaces=ns)

    if table_title != element_title.text:
        print(f"Updating Title to: {table_title}")
        element_title.text = table_title

    ### Update Spatial resolution and unit###
    table_spatial_resolution = row['Spatial resolution as integer']
    table_spatial_resolution_unit = row['Spatial resolution unit']
    element_spatial_resolution = root.find('gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution/gmd:MD_Resolution/gmd:distance/gco:Distance', namespaces=ns)

    if table_spatial_resolution != element_spatial_resolution.text:
        print(f"Updating spatial resolution integer to: {table_spatial_resolution}")
        element_spatial_resolution.text = table_spatial_resolution

    if table_spatial_resolution_unit != element_spatial_resolution.attrib.get('uom'):
        print(f"Updating spatial resolution unit to: {table_spatial_resolution_unit}")
        element_spatial_resolution.attrib['uom'] = table_spatial_resolution_unit

    # ### Update temporal extent ###
    table_temporal_extent_begin = datetime.strptime(row['start_time'], "%d_%m_%Y").date().isoformat() 
    table_temporal_extent_end = datetime.strptime(row['end_time'], "%d_%m_%Y").date().isoformat() 

    entity_temporal_begin = root.find("gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:beginPosition",
        namespaces=ns
    )
    entity_temporal_end = root.find("gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:endPosition",
        namespaces=ns
    )
    
    if table_temporal_extent_begin != entity_temporal_begin.text:
        print(f"Updating temporal extent begin to: {table_temporal_extent_begin}")
        entity_temporal_begin.text = table_temporal_extent_begin

    if table_temporal_extent_end != entity_temporal_end.text:
        print(f"Updating temporal extent end to: {table_temporal_extent_end}")
        entity_temporal_end.text = table_temporal_extent_end
    
    # #TODO: Check that time is in correct format not a string


    # ### Update MD_TopicCategoryCode ###
    table_MD_TopicCategoryCode = row['MD_TopicCategoryCode']
    element_MD_TopicCategoryCode = root.find('gmd:identificationInfo/gmd:MD_DataIdentification/gmd:topicCategory/gmd:MD_TopicCategoryCode', namespaces=ns)

    if table_MD_TopicCategoryCode != element_MD_TopicCategoryCode.text:
        print(f"Updating MD_TopicCategoryCode to: {table_MD_TopicCategoryCode}")
        element_MD_TopicCategoryCode.text = table_MD_TopicCategoryCode

    # ### Update Spatial Extent ###
    table_extent = row['Extent']
    element_east_bound = root.find('gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:eastBoundLongitude/gco:Decimal', namespaces=ns)
    element_west_bound = root.find('gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:westBoundLongitude/gco:Decimal', namespaces=ns)
    element_north_bound = root.find('gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:northBoundLatitude/gco:Decimal', namespaces=ns)
    element_south_bound = root.find('gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:southBoundLatitude/gco:Decimal', namespaces=ns)
                                                               
    if "EU" in table_extent:
        element_east_bound.text = "37.84"
        element_west_bound.text = "-25.91"
        element_north_bound.text = "71.90"
        element_south_bound.text = "33.80"

    else:
        print(f"Extent in table not recognized: {table_extent} setting to default bounds")
        element_east_bound.text = "-180.00"
        element_west_bound.text = "180.00"
        element_north_bound.text = "90.00"
        element_south_bound.text = "-90.00"

    # ### Update CRS ###
    table_crs = row['CRS']
    element_crs = root.find('gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gmx:Anchor', namespaces=ns)
    if "3035" in table_crs and "3035" in element_crs.text:
        pass

    else:
        print(f"CRS in table not recognized, can't update! {table_crs}")

    # ### Update Online Resource ###
    table_online_resource = platform_base_url + "catalogue_pages/" + row['catalogue_page'] + ".html"
    element_online_resource = root.find('gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:linkage/gmd:URL', namespaces=ns)

    if table_online_resource != element_online_resource.text:
        print(f"Updating Online Resource to: {table_online_resource}")
        element_online_resource.text = table_online_resource
                                
    ### Update lineage ###
    table_lineage = row['Lineage_statement']
    element_lineage = root.find('gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:statement/gco:CharacterString', namespaces=ns)

    if table_lineage != element_lineage.text:
        print(f"Updating Lineage statement to: {table_lineage}")
        element_lineage.text = table_lineage

    ### Update spatial representation type ###
    table_representation_type = row['Spatial_representation_type']
    element_type = root.find('gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialRepresentationType/gmd:MD_SpatialRepresentationTypeCode', namespaces=ns)
    # print(f"Current spatial representation type: {element_type.attrib.get('codeListValue')}")

    if element_type.attrib.get('codeListValue') != table_representation_type:
        print(f"Updating spatial representation type to: {table_representation_type}")
        element_type.attrib['codeListValue'] = table_representation_type

    ### Update file type ###
    table_file_type = row['File type']
    element_file_type = root.find('gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat/gmd:MD_Format/gmd:name/gco:CharacterString', namespaces=ns)
    # print(f"Current file type: {element_file_type.text}")

    if element_file_type.text != table_file_type:
        print(f"Updating file type to: {table_file_type}")
        element_file_type.text = table_file_type

    ### Update data identifier ###
    table_file_identifier = row['File identifier']
    element_file_identifier = root.find('gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:identifier/gmd:MD_Identifier/gmd:code/gco:CharacterString', namespaces=ns)
    # print(f"Current data identifier: {element_file_identifier.text}")

    if element_file_identifier.text != table_file_identifier:
        print(f"Updating data identifier to: {table_file_identifier}")
        element_file_identifier.text = table_file_identifier

    ### Update file identifier (primary key) ###
    table_file_identifier = row['File identifier']
    element_file_identifier = root.find('gmd:fileIdentifier/gco:CharacterString', namespaces=ns)
    # print(f"Current file identifier: {element_file_identifier.text}")

    if element_file_identifier.text != f"metadata_{table_file_identifier}":
        print(f"Updating file identifier to: metadata_{table_file_identifier}")
        element_file_identifier.text = f"metadata_{table_file_identifier}"
 

    # Save the updated XML back to file
    ET.register_namespace("gmd", "http://www.isotc211.org/2005/gmd")
    ET.register_namespace("gco", "http://www.isotc211.org/2005/gco")
    ET.register_namespace("gmx", "http://www.isotc211.org/2005/gmx")
    ET.register_namespace("gml", "http://www.opengis.net/gml")
    tree.write(xml_path, encoding='utf-8', xml_declaration=True)

def comman_line_router(args):
    if len(args) != 3:
        sys.exit(1)

    table_path = args[1]
    xml_path = args[2]
    # update_xml_from_table(table_path, xml_path) # FIXME

if __name__ == "__main__":
    if len(sys.argv) > 1:
        comman_line_router(sys.argv)
    
    else:
        table_path = r"C:/Users/5298954/Documents/Github_Repos/Exposome-Map-Documents/Exposome_maps_inventory/Exposome maps inventory.csv"
        df = pd.read_csv(table_path, dtype={'show_on_map': 'bool'}, on_bad_lines='skip', header=0, delimiter=';', keep_default_na=False)#, encoding='latin1')

        df.apply(lambda row: update_xml_from_row(row, row["Local path to XML file"]), axis=1)

        # xml_path = r"C:\Users\5298954\Documents\Projects\Exposure_Map\project_geoserver\metadata_xmls\metadata_for_python_development.xml"
        # xmls = [
        #         "metadata_Annual_NO2_25m",
        #         "metadata_Annual_PM10_25m",
        #         "metadata_Annual_PM25_25m",
        #         "metadata_Annual_O3_25m",
        #         "metadata_Yearly_average_temperature",
        #         "metadata_Daily_average_temperature",
        #         "metadata_Daily_minimum_temperature",
        #         "metadata_Daily_maximum_temperature",
        #         "metadata_Monthly_average_temperature",
        #         "metadata_Urban_Rural_indicator",
        #         "metadata_Annual_average_A_weighted_road_traffic_noise_estimates",
        #         "metadata_Downward_UV_radiation_at_the_surface,_monthy_mean_of_daily_average",
        #         "metadata_Downward_UV_radiation_at_the_surface,_monthly_max_of_daily_average",
        #         "metadata_Median_NDVI_within_300m",
        #         "metadata_Median_NDVI_within_500m",
        #         "metadata_Median_NDVI_within_1km",
        #         "metadata_Standard_deviation_NDVI_within_300m",
        #         "metadata_Standard_deviation_NDVI_within_500m",
        #         "metadata_Standard_deviation_NDVI_within_1km",
        #         "metadata_Mean_NDVI_within_300m",
        #         "metadata_Mean_NDVI_within_500m",
        #         "metadata_Mean_NDVI_within_1km",
        #         "metadata_Median_MSAVI_within_300m",
        #         "metadata_Median_MSAVI_within_500m",
        #         "metadata_Median_MSAVI_within_1km",
        #         "metadata_Standard_deviation_MSAVI_within_300m",
        #         "metadata_Standard_deviation_MSAVI_within_500m",
        #         "metadata_Standard_deviation_MSAVI_within_1km",
        #         "metadata_Mean_MSAVI_within_300m",
        #         "metadata_Mean_MSAVI_within_500m",
        #         "metadata_Mean_MSAVI_within_1km",
        #         "metadata_Distance_to_nearest_green_space_using_CORINE",
        #         "metadata_Distance_to_nearest_green_space_using_URBAN_ATLAS",
        #         "metadata_Light_at_night_300m_buffer",
        #         "metadata_Light_at_night_500m_buffer",
        #         "metadata_Light_at_night_1000m_buffer",
        #         "metadata_Imperviousness_300m_buffer",
        #         "metadata_Imperviousness_500m_buffer",
        #         "metadata_Imperviousness_1000m_buffer",
        #         "metadata_Distance_to_nearest_blue_space",
        #         "metadata_Distance_to_nearest_sea_ocean",
        #         "metadata_Distance_to_nearest_inland_freshwater",
        #         "metadata_Walkabiliy_300m_buffer",
        #         "metadata_Walkabiliy_500m_buffer",
        #         "metadata_Walkabiliy_1000m_buffer"
        # ]

        # xmls_base_path = f"C:\\Users\\5298954\\Documents\\Github_Repos\\\Exposome-Map-Documents\\metadata_XMLs"
        # for xml in xmls:
        #     shutil.copy2(r"C:\Users\5298954\Documents\Projects\Exposure_Map\project_geoserver\metadata_xmls\NDV_MD3_XX_XX_05_v2_metadata\a2a7b042-706e-492f-8942-5ffd8556edac\metadata\metadata.xml",
        #                 os.path.join(xmls_base_path, xml+".xml"))

