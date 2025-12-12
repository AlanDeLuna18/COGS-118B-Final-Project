def extract_info_per_measure(chart_lines):
    for line in chart_lines:
        if line.startswith("COURSE:") or line.startswith("LEVEL:"):
            continue

    measures_arr = [
        [],  # 0: notes
        [],  # 1: bpm
        [],  # 2: time signature
        [],  # 3: scroll speed
        [],  # 4: is_gogo
    ]

    current_bpm = 0
    time_sig = (4, 4)
    scroll = 1.0
    is_gogo = False

    inside_chart = False
    current_measure_notes = ""

    for raw_line in chart_lines:
        line = raw_line.strip()

        if not line or line.startswith("//"):
            continue

        # chart boundaries
        if line.startswith("#START"):
            inside_chart = True
            continue

        if line.startswith("#END"):
            inside_chart = False
            break

        if not inside_chart:
            continue

        # measure metadata
        if line.startswith("#BPMCHANGE"):
            current_bpm = float(line.split()[1])
            continue

        if line.startswith("#MEASURE"):
            num, den = line.split()[1].split("/")
            time_sig = (int(num), int(den))
            continue

        if line.startswith("#SCROLL"):
            scroll = float(line.split()[1])
            continue

        if line == "#GOGOSTART":
            is_gogo = True
            continue

        if line == "#GOGOEND":
            is_gogo = False
            continue

        # measure content
        if "," in line:
            note_part = line.replace(",", "")
            current_measure_notes += note_part

            measures_arr[0].append(current_measure_notes)
            measures_arr[1].append(current_bpm)
            measures_arr[2].append(time_sig)
            measures_arr[3].append(scroll)
            measures_arr[4].append(1 if is_gogo else 0)

            current_measure_notes = ""
        else:
            current_measure_notes += line

    return measures_arr