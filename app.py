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


def prepare_pdf(file, ids):
    delete_list = []
    page_number = 0
    with fitz.open(file) as doc:
        for page in doc:
            page_number += 1
            for id in ids:
                page_ids = page.search_for(id)
                for _ in page_ids:
                    hl = page.add_highlight_annot(_)
                    hl.update()
                    delete_list.append(page_number)
            marked_doc = "marked_" + file
            doc.save("marked_" + file)

    marked_pages = set((delete_list))

    with fitz.open(file) as doc:
        doc.delete_pages(tuple(marked_pages))
        deleted_doc = "deleted_" + file
        doc.save(deleted_doc)
    return marked_pages, marked_doc, deleted_doc


@eel.expose
def compare_files(file_csv, file_pdf):
    # file_csv = 'L1.csv'
    # file_pdf = 'P1.pdf' 
    ac, m, n = get_columns_id(file_csv)
    cleared_csv = clear_lgtc_csv(file_csv, ac)
    trip_ids = get_trip_id_csv(cleared_csv, m, n)
    prepare_pdf(file_pdf, trip_ids)
    # print("compare_files py", file_csv, file_pdf)


if __name__ == "__main__":
    eel.init('web')
    eel.start(
        'templates/index.html',
        jinja_templates='templates',
        size=(400, 600)
    )


