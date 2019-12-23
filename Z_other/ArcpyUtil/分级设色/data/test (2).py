import arcpy

if __name__ == '__main__':

    mxd = arcpy.mapping.MapDocument(r"D:\Fujian\RSPlatForm\RSPlatForm\Depend\Gansu\mxd\VEGDRI_Nation.mxd")
    df = arcpy.mapping.ListDataFrames(mxd, 'layers')[0]
    lyr = arcpy.mapping.ListLayers(mxd, "tifFile", df)[0]
    lyrFile = arcpy.mapping.Layer(lyr_reference)
    arcpy.mapping.UpdateLayer(df, lyr, lyrFile, True)
    if lyr.symbologyType == "RASTER_CLASSIFIED":
        lyr.symbology.classBreakValues = classList

    arcpy.mapping.ExportToPDF(mxd, r"E:\temp\mxd\StatePopulation.pdf")
    del mxd, lyrFile