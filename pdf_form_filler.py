import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
import pandas.io.sql as psql
import psycopg2

###Eighth working attempt - for all pages filling text fields from Text8[0] to Text22[0] with values from employees database
###Eighth working attempt - for all pages filling text fields from Text8[0] to Text22[0] with values from employees database
###Eighth working attempt - for all pages filling text fields from Text8[0] to Text22[0] with values from employees database
###Eighth working attempt - for all pages filling text fields from Text8[0] to Text22[0] with values from employees database
###Eighth working attempt - for all pages filling text fields from Text8[0] to Text22[0] with values from employees database

###         MMMMMMM     MMMMMMM        VVVV      VVVV       PPPPPPPPPPPP
###         MMMMMMMM   MMMMMMMM         VVVV    VVVV        PPPP    PPPPP
###         MMMM MMMMMMMMM MMMM          VVVV  VVVV         PPPP    PPPPP
###         MMMM  MMMMMM   MMMM           VVV  VVV          PPPPPPPPPPPPP
###         MMMM   MMMM    MMMM            VVVVVV           PPPP
###         MMMM           MMMM             VVVV            PPPP
###         MMMM           MMMM              VV             PPPP


# Conneect to an existing databasee
conn = psycopg2.connect("credentials")


emp_database_df = psql.read_sql('SELECT * FROM employees', conn)
df = emp_database_df

company_data = pd.read_excel("path to company data in excel file","Sheet2",header=0)


writer = PdfWriter()
reader2 = PdfReader("path to .pdf form file")
fields2 = reader2.get_fields()
#x2 = fields2.items()

count = 0
for j in range(len(reader2.pages)):
    page = reader2.pages[j]
    fields2 = reader2.get_fields()
    #print(fields2)

    writer.add_page(page)


    for i in fields2.keys():
        #print(i)

        v = fields2[str(i)]["/T"]

        if "Text" in v and count in range(8):
            writer.update_page_form_field_values(
                writer.pages[j], {v:f"{company_data.iloc[count][1]}"}
            )
            #print(f"{company_data.iloc[count][1]}")

    
        count += 1



# write "output" to PyPDF2-output.pdf
with open("output .pdf file", "wb") as output_stream:
    writer.write(output_stream)
