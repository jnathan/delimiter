import cStringIO
import sys

import nose
from nose.tools import *

import delimiter_reader

@raises(ValueError)
def test_row_birthdate_to_ts_1():
    dr = delimiter_reader.DelimiterReader()
    row = ['Simpson', 'Homer', 'Male', 'Orange', '123']
    dr.row_birthdate_to_ts(row)

def test_row_birthdate_to_ts_2():
    dr = delimiter_reader.DelimiterReader()
    row = ['Simpson', 'Homer', 'Male', 'Orange', '5/12/1956']
    row_birthdate_ts = dr.row_birthdate_to_ts(row)
    assert_equal(row_birthdate_ts, ['Simpson', 'Homer', 'Male', 'Orange', -430423200L])

@raises(delimiter_reader.DelimiterReaderException)
def test_read_file1():
    dr = delimiter_reader.DelimiterReader()
    dr.read_file('asasdfa')

def test_read_file2():
    sys.path.append('test')
    import test_read_file2_rows
    dr = delimiter_reader.DelimiterReader()
    dr.read_file('test/test_read_file2_space.dat')
    assert_equal(dr.rows, test_read_file2_rows.rows)
    sys.path.pop()

def test_read_rows1():
    sys.path.append('test')
    import test_read_rows1
    dr = delimiter_reader.DelimiterReader()
    sample_csv_rows = """Sinclair,Quyen,Female,Red,6/8/1980
Fajardo,Lila,Female,Pink,7/11/1957
Lebow,Sang,Male,Yellow,11/21/1964
Jasinski,Emile,Male,Brown,6/5/1964
Rippeon,Vicki,Female,Purple,10/28/1999
Kindel,Kimber,Female,Black,1/21/1950
Botello,Julio,Male,White,2/1/1949
Sharma,Troy,Female,Blue,10/13/1944
Adrian,Earleen,Female,Brown,11/3/2014
Casillas,Ariel,Male,Blue,6/31/2016
Mayer,Mike,Female,Green,9/7/1981
Edgell,Hank,Male,Orange,2/1/1975
Matheson,Shemeka,Female,Yellow,8/19/2008
Sallee,Felton,Male,Blue,6/31/1948
Cahoon,Hal,Male,Purple,1/28/1949
Gourley,Lynwood,Male,Orange,9/6/2004
Browning,Theo,Male,Black,4/2/1969
Do,Reinaldo,Male,Pink,9/28/2000
Lipscomb,Shu,Female,Yellow,11/23/1992
Makela,Kirstin,Female,Gray,7/26/1963
Ortez,Steven,Male,Red,8/13/2000
Achenbach,Tony,Male,Blue,5/18/1985
Recinos,Paz,Female,Brown,1/3/1962
Nakano,Son,Female,White,2/10/2009
Nuckols,Chase,Male,Blue,8/5/1957
Padilla,Micki,Female,Black,1/18/1951
Kimbrough,Brooks,Male,Gray,3/3/1980"""
    in_fd = cStringIO.StringIO(sample_csv_rows)
    dr.read_rows(in_fd)
    assert_equal(dr.rows, test_read_rows1.rows)
    sys.path.pop()

def test_sort_gender_then_lastname():
    sys.path.append('test')
    import test_sort_gender_then_lastname
    dr = delimiter_reader.DelimiterReader()
    sample_pipe_rows = """Ruley|Cedrick|Male|Red|10/15/1979
Fleener|Matthew|Male|Green|2/13/1966
Pittard|Adan|Male|Brown|12/13/1965
Quintero|Marty|Male|Black|5/11/1967
Demko|Celena|Female|Green|1/21/1922
Summers|Ramon|Male|Red|4/8/1939
Aten|Clifton|Male|Black|5/24/2013
Cork|Kenny|Male|Green|10/27/1965
Gaddis|Michel|Male|Yellow|12/7/2005
Straughter|Aurea|Female|Green|1/25/2012
Kautz|Delbert|Male|Brown|6/1/1967
Millan|Emmanuel|Male|Red|2/13/1973
Thiel|Markus|Male|Blue|4/17/1948
Timko|Diamond|Female|Brown|6/27/1950
Wyman|Barbie|Female|Black|4/26/1978
Morley|Debbie|Female|Black|3/19/1949
Buell|Kizzy|Female|Orange|7/16/1942
Ferreira|Leeanne|Female|Green|4/25/1973
Winger|Natalie|Female|Yellow|4/22/2000
Jeon|Kathleen|Female|Black|3/30/1934
Ma|Kandra|Female|Yellow|10/3/2015
Heiser|Tama|Female|Purple|4/20/1938
Hunsucker|Krystyna|Female|Purple|6/23/1953
Cottle|Loren|Female|Gray|7/26/1982
Robichaud|Teddy|Male|Yellow|7/6/1952
Lewter|Sarina|Female|White|6/5/1995
Eadie|Jacques|Male|Brown|3/31/2011"""
    in_fd = cStringIO.StringIO(sample_pipe_rows)
    dr.read_rows(in_fd)
    dr.sort_gender_then_lastname()
    assert_equal(dr.rows, test_sort_gender_then_lastname.rows)
    sys.path.pop()

def test_sort_birthdate():
    sys.path.append('test')
    import test_sort_birthdate
    dr = delimiter_reader.DelimiterReader()
    sample_space_rows = """Whittenburg Elliot Male Blue 2/17/1937
Tubbs Mertie Female Pink 7/16/1957
Garbutt Vida Female Red 2/20/1954
Dwight Boyce Male White 12/2/1942
Craney Mario Male Orange 5/15/1946
Regner Luz Female Pink 8/28/1950
Kring Han Female Purple 8/25/2009
Boissonneault Jeanice Female Orange 11/11/1951
Mallette Emmitt Male Pink 6/27/1995
Zermeno Wes Male Orange 7/10/1927
Berwick Hung Male White 10/7/1973
Knupp Darci Female Gray 9/2/1954
Fagin Josette Female Green 6/9/1970
Osuna Norris Male Orange 10/28/2009
Legler Mario Male Black 1/31/1947
Lummus Caprice Female Pink 5/10/1920
Isaacson Bernardo Male Black 10/12/1929
Thome Marcellus Male Green 11/25/1945
Eckhart Carolin Female Red 3/12/1930
Schulze Malorie Female Yellow 6/28/2009
Stainbrook Ellis Female Gray 12/30/1928
Humes Marilyn Female Black 12/10/1962
Hepp Lorilee Female Red 8/10/2002
Ennis Emery Male Orange 8/14/1998
Bellinger Mohamed Male Gray 7/18/1971"""
    in_fd = cStringIO.StringIO(sample_space_rows)
    dr.read_rows(in_fd)
    dr.sort_birthdate()
    assert_equal(dr.rows, test_sort_birthdate.rows)
    sys.path.pop()

def test_sort_gender():
    sys.path.append('test')
    import test_sort_gender
    dr = delimiter_reader.DelimiterReader()
    sample_csv_rows = """Scoggins,Galen,Male,Black,7/3/1931
Bella,Darrell,Male,Orange,11/2/1942
Newborn,Chuck,Male,Pink,4/26/1920
Nelsen,Clyde,Male,Yellow,8/23/1974
Glaser,Henry,Male,White,10/26/1990
Huseman,Fabian,Male,Purple,6/15/2001
Yamada,Landon,Male,Black,11/22/2004
Kurt,Dallas,Female,Blue,7/6/1941
Gladden,Leonarda,Female,Red,9/4/1995
Mena,Dexter,Male,Pink,12/30/2005
Arteaga,Eusebio,Male,Black,2/23/2013
Thorson,Trista,Female,Gray,2/8/2002
Daughtry,Wilson,Male,Purple,11/5/1953
Provost,Eric,Male,Red,5/7/1935
Grillo,Felica,Female,Orange,5/19/1950
Mackay,Barney,Male,Red,9/8/1964
Franks,Al,Male,Green,5/19/1920
Bermudez,Willian,Male,Brown,6/20/1948
Paynter,Lacy,Male,Brown,10/26/2005
Swinton,Orval,Male,Brown,4/4/1995
Spina,Cira,Female,Purple,7/3/1965"""
    in_fd = cStringIO.StringIO(sample_csv_rows)
    dr.read_rows(in_fd)
    dr.sort_gender()
    assert_equal(dr.rows, test_sort_gender.rows)
    sys.path.pop()

def test_sort_lastname1():
    sys.path.append('test')
    import test_sort_lastname1
    dr = delimiter_reader.DelimiterReader()
    sample_pipe_rows = """Hash|Mayra|Female|Purple|3/29/1989
Relyea|Lasonya|Female|Gray|1/12/1972
Feely|Danny|Male|White|7/17/1921
Cerrato|Charisse|Female|Purple|2/19/2002
Mcglynn|Omar|Male|Blue|2/6/1995
Cusumano|Robby|Male|Orange|11/11/2000
Donofrio|Deanna|Female|Red|6/25/2011
Biddle|Pauletta|Female|Green|1/20/1995
Duquette|Edwin|Male|Orange|12/31/2017
Kidd|Julieta|Female|Yellow|1/14/1977
Houston|Numbers|Male|Yellow|3/20/1997
Hodo|Edris|Female|Green|1/20/1952
Osborn|Christiane|Female|White|7/22/1931
Kowal|Kia|Female|Pink|2/11/1956
Dustin|August|Male|Black|6/3/1996
Trinkle|Camelia|Female|Black|3/26/2013
Dorman|Terresa|Female|Gray|8/8/1936
Hofman|Nikki|Female|Green|9/29/1949
Partridge|Jone|Female|Black|10/9/1939
Marable|Marc|Male|Black|4/7/1928
Mcglade|Fairy|Female|Brown|11/3/1931
Hendry|Mandi|Female|Purple|7/9/1943
Osullivan|Ashley|Female|White|8/10/2013
Cadogan|Gricelda|Female|Yellow|11/16/1934"""
    in_fd = cStringIO.StringIO(sample_pipe_rows)
    dr.read_rows(in_fd)
    dr.sort_lastname()
    assert_equal(dr.rows, test_sort_lastname1.rows)
    sys.path.pop()

def test_sort_lastname2():
    sys.path.append('test')
    import test_sort_lastname2
    dr = delimiter_reader.DelimiterReader()
    sample_space_rows = """Regner Luz Female Pink 8/28/1950
Kring Han Female Purple 8/25/2009
Boissonneault Jeanice Female Orange 11/11/1951
Mallette Emmitt Male Pink 6/27/1995
Zermeno Wes Male Orange 7/10/1927
Berwick Hung Male White 10/7/1973
Knupp Darci Female Gray 9/2/1954
Fagin Josette Female Green 6/9/1970
Osuna Norris Male Orange 10/28/2009
Legler Mario Male Black 1/31/1947
Lummus Caprice Female Pink 5/10/1920
Isaacson Bernardo Male Black 10/12/1929
Thome Marcellus Male Green 11/25/1945
Eckhart Carolin Female Red 3/12/1930
Schulze Malorie Female Yellow 6/28/2009
Stainbrook Ellis Female Gray 12/30/1928
Humes Marilyn Female Black 12/10/1962
Hepp Lorilee Female Red 8/10/2002
Ennis Emery Male Orange 8/14/1998"""
    in_fd = cStringIO.StringIO(sample_space_rows)
    dr.read_rows(in_fd)
    dr.sort_lastname(descending=True)
    assert_equal(dr.rows, test_sort_lastname2.rows)
    sys.path.pop()
