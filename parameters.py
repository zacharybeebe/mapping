INITIAL_FRAME_LAYOUT = {'FT': [0, 0, 1.0, 0.07],
                        'FS': [0, 0.07, 0.18, 1-0.07],
                        'FM': [0.18, 0.07, 1-0.18, 1-0.07]}




BLACK = '#000000'
RED = '#FF0000'
DARKRED = '#A10C0C'
GREY = '#E1E1E1'
WHITE = '#FFFFFF'
FORESTGREEN = '#418A52'
PALEGREEN = '#CCFFE5'
SEAGREEN = '#99FFCC'
DSEAGREEN = '#0DE3A4'
ORANGESOFT = '#FBECB4'
ORANGEMED = '#FADC6F'


SHP_FIELDS = ['TIMBER_TRU', 'UNIT_NM', 'ACRES1', 'MBF']



font_name = 'Calibri'

font5Cb = (font_name, "5", "bold")
font6Cb = (font_name, "6", "bold")
font7Cb = (font_name, "7", "bold")
font7_5Cb = (font_name, "7.5", "bold")
font8Cb = (font_name, "8", "bold")
font10Cb = (font_name, "10", "bold")
font11Cb = (font_name, "11", "bold")
font12Cb = (font_name, "12", "bold")
font13Cb = (font_name, "13", "bold")
font14Cb = (font_name, "14", "bold")
font18Cb = (font_name, "18", "bold")
font24Cb = (font_name, "24", "bold")
font36Cb = (font_name, "36", "bold")

FONT_DICT = {'font5': font5Cb,
             'font6': font6Cb,
             'font7': font7Cb,
             'font8': font8Cb,
             'font10': font10Cb,
             'font11': font11Cb,
             'font12': font12Cb,
             'font14': font14Cb,
             'font18': font18Cb,
             'font36': font36Cb}



NAD_1983_WA_S = """PROJCS["NAD_1983_HARN_StatePlane_Washington_South_FIPS_4602_Feet",
                   GEOGCS["GCS_North_American_1983_HARN",DATUM["D_North_American_1983_HARN",
                   SPHEROID["GRS_1980",6378137.0,298.257222101]],
                   PRIMEM["Greenwich",0.0],
                   UNIT["Degree",0.0174532925199433]],
                   PROJECTION["Lambert_Conformal_Conic"],
                   PARAMETER["False_Easting",1640416.666666667],
                   PARAMETER["False_Northing",0.0],
                   PARAMETER["Central_Meridian",-120.5],
                   PARAMETER["Standard_Parallel_1",45.83333333333334],
                   PARAMETER["Standard_Parallel_2",47.33333333333334],
                   PARAMETER["Latitude_Of_Origin",45.33333333333334],
                   UNIT["Foot_US",0.3048006096012192]],
                   VERTCS["NAVD_1988",VDATUM["North_American_Vertical_Datum_1988"],
                   PARAMETER["Vertical_Shift",0.0],PARAMETER["Direction",1.0],
                   UNIT["Foot_US",0.3048006096012192]]""".replace('\n', '').replace(' ', '')

