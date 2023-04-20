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

class Point4D:
    def __init__(self, id, x, y, z, w):
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def log(self):
        print_point = "Point {} with coordinates: ({}, {}, {}, {})".format(self.id, self.x, self.y, self.z, self.w)
        return print_point

    def dominates(self, p):
        return self.x <= p.x and self.y <= p.y and self.z <= p.z and self.w <= p.w

class Point5D:
    def __init__(self, id, x1, x2, x3, x4, x5):
        self.id = id
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.x4 = x4
        self.x5 = x5

    def log(self):
        print_point = "Point {} with coordinates: ({}, {}, {}, {}, {})".format(self.id, self.x1, self.x2, self.x3, self.x4, self.x5)
        return print_point

    def dominates(self, p):
        return self.x1 <= p.x1 and self.x2 <= p.x2 and self.x3 <= p.x3 and self.x4 <= p.x4 and self.x5 <= p.x5


class Point10D:
    def __init__(self, id, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10):
        self.id = id
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.x4 = x4
        self.x5 = x5
        self.x6 = x6
        self.x7 = x7
        self.x8 = x8
        self.x9 = x9
        self.x10 = x10


    def log(self):
        print_point = "Point {} with coordinates: ({}, {}, {}, {}, {}, {}, {}, {}, {}, {})".\
            format(self.id, self.x1, self.x2, self.x3, self.x4, self.x5, self.x6, self.x7, self.x8, self.x9, self.x10)
        return print_point

    def dominates(self, p):
        return self.x1 <= p.x1 and self.x2 <= p.x2 and self.x3 <= p.x3 and self.x4 <= p.x4 and self.x5 <= p.x5 and self.x6 <= p.x6 and self.x7 <= p.x7 and self.x8 <= p.x8 and self.x9 <= p.x9 and self.x10 <= p.x10


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
    elif d == 4:
        for i in range(n):
            data.add_point(Point4D(df.iloc[i].name, df.iloc[i][0], df.iloc[i][1], df.iloc[i][2], df.iloc[i][3]))
    elif d == 5:
        for i in range(n):
            data.add_point(Point5D(df.iloc[i].name, df.iloc[i][0], df.iloc[i][1], df.iloc[i][2], df.iloc[i][3], df.iloc[i][4]))
    elif d == 10:
        for i in range(n):
            data.add_point(Point10D(df.iloc[i].name, df.iloc[i][0], df.iloc[i][1], df.iloc[i][2], df.iloc[i][3],
                                   df.iloc[i][4], df.iloc[i][5], df.iloc[i][6], df.iloc[i][7],
                                   df.iloc[i][8], df.iloc[i][9]))

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

        if dim == 4:
            for skyp in skyline.points:
                d[fieldnames[0]] = skyp.id
                d[fieldnames[1]] = skyp.x
                d[fieldnames[2]] = skyp.y
                d[fieldnames[3]] = skyp.z
                d[fieldnames[4]] = skyp.w
                writer.writerow(d)

        if dim == 5:
            for skyp in skyline.points:
                d[fieldnames[0]] = skyp.id
                d[fieldnames[1]] = skyp.x1
                d[fieldnames[2]] = skyp.x2
                d[fieldnames[3]] = skyp.x3
                d[fieldnames[4]] = skyp.x4
                d[fieldnames[5]] = skyp.x5
                writer.writerow(d)

        if dim == 10:
            for skyp in skyline.points:
                d[fieldnames[0]] = skyp.id
                d[fieldnames[1]] = skyp.x1
                d[fieldnames[2]] = skyp.x2
                d[fieldnames[3]] = skyp.x3
                d[fieldnames[4]] = skyp.x4
                d[fieldnames[5]] = skyp.x5
                d[fieldnames[6]] = skyp.x6
                d[fieldnames[7]] = skyp.x7
                d[fieldnames[8]] = skyp.x8
                d[fieldnames[9]] = skyp.x9
                d[fieldnames[10]] = skyp.x10
                writer.writerow(d)