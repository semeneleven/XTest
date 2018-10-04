import random

def satellite(vector, error_poses):
    errors = []
    for error_pos in error_poses:
        if error_pos not in errors:
            errors.append(error_pos)
    sorted(errors, reverse=True)
    error_vector = '0'*len(vector)
    for error in errors :
        error_vector = error_vector[:len(vector)-error]+'1'+'0'*error
    satellite = bin(int(vector, 2) ^ int(error_vector, 2))[2:]
    satellite = '0'*(len(vector)-len(satellite)) + satellite
    return satellite

# vector = str(code) satellites = [str(satellite),...] code_distance = number
def assert_code(vector, satellites, code_distance):
    for satellite in satellites:
        error_vector = bin(int(vector, 2) ^ int(satellite, 2))[2:]
        if error_vector.count('1') != code_distance :
            return False
    return True

# vector = str(code) satellites = [str(satellite),...] ans = [number(index of satellites with min code_distance),...]
def assert_decode(vector, satellites, ans):
    sorted(ans)
    code_distances = []
    for satellite in satellites:
        error_vector = bin(int(vector, 2) ^ int(satellite, 2))[2:]
        code_distances.append(error_vector.count('1'))
    min_code_distances = [i for i, x in enumerate(code_distances) if x == min(code_distances)]
    if min_code_distances == ans:
        return True
    else :
        return False

def generate_to_encode():
    length = random.randint(8,12)
    code_distance = random.randint(1,3)
    vector = ''
    for i in range(length) :
        vector += str(random.randint(0,1))
    return vector, code_distance

def generate_to_decode():
    vector = generate_to_encode()[0]
    satellites = []
    code_distances = get_code_distances()
    for code_distance in code_distances:
        error_poses = []
        for i in range(code_distance):
            rand = random.randint(0, len(vector)-1)
            if rand not in error_poses:
                error_poses.append(rand)
        satellites.append(satellite(vector, error_poses))
    return vector, satellites

def get_code_distances():
    code_distances = []
    for i in range(6):
        code_distances.append(random.randint(1,4))
    return code_distances



# tests
print(satellite('00010101',[2,4,1]))
print(assert_code('11010101',['10110101','00010101'],2))
print(generate_to_encode())
print(generate_to_decode())
print(assert_decode('00010101111',['00110101111', '00010101110', '10010101111', '11110101111', '00010101101', '10010100111'],[0,1,2,4]))