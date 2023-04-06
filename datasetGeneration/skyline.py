import pandas as pd
import csv


class DataSet:
    def __init__(self):
        self.points = []

    def log(self):
        for p in self.points:
            print(p.log())

    def add_point(self, p):
        self.points.append(p)


class Point2D:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def log(self):
        print_point = "Point {} with coordinates: ({}, {})".format(self.id, self.x, self.y)
        return print_point

    def dominates(self, p):
        return self.x <= p.x and self.y <= p.y


class Point3D:
    def __init__(self, id, x, y, z):
        self.id = id
        self.x = x
        self.y = y
        self.z = z

    def log(self):
        print_point = "Point {} with coordinates: ({}, {}, {})".format(self.id, self.x, self.y, self.z)
        return print_point

    def dominates(self, p):
        return self.x <= p.x and self.y <= p.y and self.z <= p.z


def skyline_calculation(df):
    window = DataSet()
    skyline = DataSet()
    data = DataSet()

    n = df.shape[0]
    d = df.shape[1]

    if d == 2:
        for i in range(n):
            data.add_point(Point2D(df.iloc[i].name, df.iloc[i][0], df.iloc[i][1]))
    elif d == 3:
        for i in range(n):
            data.add_point(Point3D(df.iloc[i].name, df.iloc[i][0], df.iloc[i][1], df.iloc[i][2]))

    dominanceComparisons = 0

    exit = False
    for point in data.points:
        # print("----------------NEW POINT----------------")
        # print(point.myfunc())
        # print("-----------------------------------------")

        exit = False
        for p in window.points:
            dominanceComparisons += 1
            if p.dominates(point):
                # 1) If some point p in window dominates point, then point is immediately discarded
                exit = True

        if not exit:
            # 2) If point dominates some point in W, all such points are removed from W and point is inserted into W
            for i in reversed(range(len(window.points))):
                if point.dominates(window.points[i]):
                    dominanceComparisons += 1
                    window.points.remove(window.points[i])

            # 3) If none of the above two cases holds, then point is inserted into W
            window.add_point(point)

        # print("Points currently in the window:")
        # window.myfunc()

    skyline = window

    # print("The number of comparisons are: {}".format(dominanceComparisons))

    print("The skyline points are: {0:d}".format(len(skyline.points)))
    # skyline.log()

    return skyline


def create_and_save_skyline(output_filename):

    df = pd.read_csv(output_filename, sep=',', index_col=0)

    skyline = skyline_calculation(df)

    with open('skyline.csv', mode='w', newline='') as csv_file:
        fieldnames = list(df.columns)
        fieldnames.insert(0, 'id')

        d = {}
        for i in fieldnames:
            d[i] = 0

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        dim = df.shape[1]
        if dim == 2:
            for skyp in skyline.points:
                d[fieldnames[0]] = skyp.id
                d[fieldnames[1]] = skyp.x
                d[fieldnames[2]] = skyp.y
                writer.writerow(d)

        if dim == 3:
            for skyp in skyline.points:
                d[fieldnames[0]] = skyp.id
                d[fieldnames[1]] = skyp.x
                d[fieldnames[2]] = skyp.y
                d[fieldnames[3]] = skyp.z
                writer.writerow(d)