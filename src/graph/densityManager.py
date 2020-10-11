class DensityManager():

    # 연산을 위해 depth별 딕셔너리 저장할 딕셔너리
    binary_set = {}

    # 카운트 4 이상인 idx들을 list로 저장
    absolute_index_list = []

    # 연속되는 idx 하나의 구간으로 묶기
    start_point_list = []
    end_point_list = []

    # 각 블럭 하나의 리스트로 묶기
    absolute_block_list = []


    def __init__(self):
        pass


    def densityTest(self, idx_length, divide_block_list, c, count_limit):

        for i in range(idx_length+1):
            self.binary_set[i] = 0

        for depth, block_list_by_the_depth in enumerate(divide_block_list):
            # if depth < 7:
            #     continue

            for block in block_list_by_the_depth:
                # print(block) # 확인용

                # 구간길이상수 곱해서 스타트/엔드 포인트 정확히 지정하기
                start_point = int(block['climbIdx']) * c
                end_point = int(block['fallIdx']) * c
                # 끝 값이 idx 길이를 초과하는 경우
                if end_point > idx_length:
                    end_point = idx_length

                # 블록에 속하는 구간 값 증가
                for j in range(start_point, end_point+1):
                    self.binary_set[j] += 1

        for idx, count in self.binary_set.items():
            if count >= count_limit :
                self.absolute_index_list.append(idx)

        if self.absolute_index_list[1] == self.absolute_index_list[0] +1:
            self.start_point_list.append(self.absolute_index_list[0])
        for i in range(1, len(self.absolute_index_list)-1):
            if self.absolute_index_list[i-1] != self.absolute_index_list[i]-1 and self.absolute_index_list[i+1] == self.absolute_index_list[i]+1:
                self.start_point_list.append(self.absolute_index_list[i])
            elif self.absolute_index_list[i-1] == self.absolute_index_list[i]-1 and (self.absolute_index_list[i+1] != self.absolute_index_list[i]+1):
                self.end_point_list.append(self.absolute_index_list[i])
        if self.absolute_index_list[-1] == self.absolute_index_list[-2] +1:
            self.end_point_list.append(self.absolute_index_list[-1])

        # 확인
        num_of_start = len(self.start_point_list)
        num_of_end = len(self.end_point_list)
        if num_of_start == num_of_end:
            num_of_block = num_of_start
            print("block detect success")
        else:
            num_of_block = -1
            print("block detect failed")

        for i in range(num_of_block):
            block = [self.start_point_list[i], self.end_point_list[i]]
            self.absolute_block_list.append(block)


    def getAbsolutBlockList(self):
        return self.absolute_block_list

