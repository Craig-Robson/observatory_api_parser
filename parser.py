
import json


def check_for_multiple_lines(text):
    """Checks to see if multiple sensor records are inluded in the API response
    """

    break_list = []
    count = 0
    for i in range(0, len(text)):
        line = text[i]

        if line[0:5] == '# End':
            break_list.append(i)

    return break_list


def read_request_response(sensor_text):
    """Take a .csv responce from the Sheffield UO and convert to .geojson format
    """
    data = []
    column_descriptors = {}

    for line in sensor_text:

        if line == '<pre>' or len(line) == 0:
            pass

        elif line[0] != '#':  # this is the actual data for the sensor

            seconds = line.split(',')[0]
            value = datetime.datetime.fromtimestamp(int(seconds))
            date_time = value.strftime('%Y-%m-%d %H:%M:%S')
            data.append(line+','+date_time)

        else:
            if 'sensor.family:' in line:
                family = line.split(':')[1].strip()
            elif 'site.id:' in line:
                site_name = line.split(':')[1].strip()
            elif 'From:' in line:
                from_ = line.split(': ')[1].strip()
            elif 'To:' in line:
                to_ = line.split(': ')[1].strip()
            elif 'site.longitude' in line:
                longitude = line.split(': ')[1].replace(' [deg]', '')
            elif 'site.latitude' in line:
                latitude = line.split(': ')[1].replace(' [deg]', '')
            elif 'site.heightAboveSeaLevel' in line:
                hasl = line.split(':')[1].replace(' [m]', '')
            elif 'sensor.heightAboveGround' in line:
                hag = line.split(':')[1].replace(' [m]', '')
            elif 'sensor.detectors' in line:
                detectors = line.split(': ')[1]
            elif 'ColDescription' in line:
                col = line.split(': ')[1]
                descriptor_keys = col.split(' / ')
            elif 'Column_' in line[2:9]:

                line = line.split('/ ')
        
                column_dtls = {}

                for i in range(1, len(line)):
                    column_dtls[descriptor_keys[i - 1]] = line[i]
                column_descriptors[line[0][2:]] = column_dtls

    geom = {"0": "POINT (%s %s)" % (longitude, latitude)}

    json_ = {
        'Sensor Name': {"0": '%s' % site_name},
        'Location (WKT)': geom,
        "Sensor Height Above Ground": {"0": '%s' % hag},
        "Raw ID": {"0": "%s" % site_name},
        'data': data,
        "Sensor Centroid Longitude": {"0": "%s" % longitude},
        "Sensor Centroid Latitude": {"0": "%s" % latitude},
        'family': family,
        'from': from_,
        'to': to_,
        'detectors': detectors,
        'column_metatdata': column_descriptors,
    }

    return json.dumps(json_)


def main(text):
    """Converts a text string from a successful API call to the Sheffield Urban Observatories into json matching the format of the json returned from the Newcastle Urban Observatory API.
    """
    response_text = text.splitlines()
    break_points = check_for_multiple_lines(response_text)

    output_ = []
    bp = 0
    for break_point in break_points:
        json_ = read_request_response(response_text[bp:break_point])
        bp = break_point
        output_.append(json_)
    output = {'sensors': output_}

    return output
