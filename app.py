import eel
import csv
import fitz

def get_columns_id(file_name):
    req_fields = ('Amount', 'Trip ID', 'Trip Leg')
    line_count = 0
    column_index = 0
    with open(file_name) as file:
        reader = csv.reader(file)
        for line in reader:
            if line_count==0:
                line_count += 1
            else:
                break
            for column in line:
                if req_fields[0] == column:
                    ac = column_index
                if req_fields[1] == column:
                    m = column_index
                if req_fields[2] == column:
                    n = column_index
                column_index += 1
    return ac, m, n


def clear_lgtc_csv(file_name, ac):
    with open(file_name) as csv_file_origin:
        cleared_scv = "cleared_" + file_name

        with open(cleared_scv, "w") as csv_file_cleared:
            csv_reader = csv.reader(csv_file_origin)
            csv_writer = csv.writer(csv_file_cleared)

            line_index = 0
            for record in csv_reader:
                if record[ac] != "$0.00":
                    csv_writer.writerow(record)
    return cleared_scv


def get_trip_id_csv(file_name, m, n):
    trips_id = []
    with open(file_name) as csv_file_origin:
        reader = csv.reader(csv_file_origin)
        line_index = 0
        for line in reader:
            if line_index > 0:
                trips_id.append("1-" + line[m] + "-" + line[n])
            line_index += 1
    return trips_id

def hl_pdf(file, ids):
    with fitz.open(file) as doc:
        for page in doc:
            for id in ids:
                res = page.search_for(id)
                # print(res)
                # print(type(res))
                if len(res) > 0:
                    hl = page.add_highlight_annot(res)
                    hl.update()
        doc.save("marked_{}".format(str(file)))


# Find much on page return true
def find_id(page, ids):
        for id in ids:
            if len(page.search_for(id))>0:
                # print("Find {} on {} page.".format(id, page.number))
                return True
        return False

def remove_page(file, ids):
    with fitz.open(file) as doc:
        doc_pages=list(range(doc.page_count))
        for page in doc:
            if find_id(page, ids) or not page.get_text():
                doc_pages.remove(page.number)
        doc.select(doc_pages)
        filename='deleted_{}'.format(str(file))
        doc.save(filename)
#         check_pdf(filename, ids) 

# def check_pdf(file, ids):
#     with fitz.open(file) as doc:
#         for page in doc:
#             for id in ids:
#                 if len(page.search_for(id))>0:
#                     print("MISS on page {page}, id: {id}".format(id, page.number))

@eel.expose
def compare_files(file_csv, file_pdf):
    ac, m, n = get_columns_id(file_csv)
    cleared_csv = clear_lgtc_csv(file_csv, ac)
    trip_ids = get_trip_id_csv(cleared_csv, m, n)
    hl_pdf(file_pdf, trip_ids)
    remove_page(file_pdf, trip_ids)



if __name__ == "__main__":
    eel.init('web')
    eel.start(
        'templates/index.html',
        jinja_templates='templates',
        size=(400, 600)
    )


