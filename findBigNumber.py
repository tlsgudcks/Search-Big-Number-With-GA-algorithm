# ------ GA Programming -----
# 00000 00000부터 11111 11111까지 가장 큰 이진 정수를 GA로 찾기
# 탐색 중에 해집단의 해들이 일정 비율 동일하게 수렴하면 최적 해로 수렴했다고 판단하고 탐색을 종료하도록 설계
# ---------------------------

# ----- 제약사항 ------
# pandas 모듈 사용 금지
# random 모듈만 사용, 필요시 numpy 사용 가능
# [chromosome, fitness]로 구성된 list 타입의 해 사용: ["1010", 10]
# population 형태는 다음과 같이 list 타입으로 규정: [["1010", 10], ["0001", 1], ["0011", 3]]
# --------------------
"""
01001 10110
1의 자리가 1이면 1더함
10의 자리가 1이면 3더함
100의 자리가 1이면 4더함
1000의 자리가 1이면 
"""
import random

# ----- 수정 가능한 파라미터 -----

params = {
    'MUT': 0.5,  # 변이확률(%)
    'END' : 0.9,  # 설정한 비율만큼 chromosome이 수렴하면 탐색을 멈추게 하는 파라미터 (%)
    'POP_SIZE' : 100,  # population size 10 ~ 100
    'RANGE' : 10, # chromosome의 표현 범위, 만약 10이라면 00000 00000 ~ 11111 11111까지임
    'NUM_OFFSPRING' : 5 # 한 세대에 발생하는 자식 chromosome의 수
    # 원하는 파라미터는 여기에 삽입할 것
    }
# ------------------------------

class GA():
    def __init__(self, parameters):
        self.params = {}
        for key, value in parameters.items():
            self.params[key] = value

    def get_fitness(self, chromosome):
        fitness = 0
        for i in range(self.params["RANGE"]):
                fitness=fitness+int(chromosome[i])*2**(self.params["RANGE"]-1-i)
        # todo: 이진수 -> 십진수로 변환하여 fitness 구하기
        return fitness

    def print_average_fitness(self, population):
        # todo: population의 평균 fitness를 출력
        population_average_fitness = 0
        total_population=0
        for i in range(self.params["POP_SIZE"]):
            total_population=total_population+population[i][1]
        population_average_fitness=total_population/self.params["POP_SIZE"]
        print("population 평균 fitness: {}".format(population_average_fitness))

    def sort_population(self, population):
        population.sort(key=lambda x:x[1],reverse=True)
        # todo: fitness를 기준으로 population을 내림차순 정렬하고 반환
        
        return population

    def selection_operater(self, population):
        # todo: 본인이 원하는 선택연산 구현(룰렛휠, 토너먼트, 순위 등), 선택압을 고려할 것, 한 쌍의 부모 chromosome 반환
        mom_ch = ""
        dad_ch = ""
        """
        fitness_population=population[:]#리스트 복사
        #유전자별 적합도를 입력
        for i in range(self.params["POP_SIZE"]):
            fitness_population[i][1]=(100+(i)*(-100)/self.params["POP_SIZE"]-1)
        #유전자의 적합도 총합 계산
        total_score=0
        for i in range(self.params["POP_SIZE"]):
            total_score=fitness_population[i][1]+total_score
        #랜덤함수 호출
        k=random.randint(0, total_score)
        #랜덤함수가 해당 위치에 적용
        sum_fitness=0
        for i in range(self.params["POP_SIZE"]):
            sum_fitness=sum_fitness+fitness_population[i][1]
            if sum_fitness>k:
                dad_ch=fitness_population[i][0]
                break
        """
        mom_ch=population[random.randint(0,50)][0]
        dad_ch=population[random.randint(0,50)][0]
        
        return mom_ch, dad_ch

    def crossover_operater(self, mom_cho, dad_cho):
        # todo: 본인이 원하는 교차연산 구현(point, pmx 등), 자식해 반환
        """ 일점 교차를 사용함"""
        cut=random.randint(1, 8)
        offspring_cho = mom_cho[:cut]+dad_cho[cut:]
        
        return offspring_cho

    def mutation_operater(self, chromosome):        
        # todo: 변이가 결정되었다면 chromosome 안에서 랜덤하게 지정된 하나의 gene를 반대의 값(0->1, 1->0)으로 변이
        mutation_gene=random.randint(0, 9)
        print("변이발생")
        if chromosome[mutation_gene]=='0':
            chromosome=chromosome[:mutation_gene]+'1'+chromosome[mutation_gene+1:]
        else:
            chromosome=chromosome[:mutation_gene]+'0'+chromosome[mutation_gene+1:]
        result_chromosome = chromosome
        return result_chromosome

    def replacement_operator(self, population, offsprings):
        # todo: 생성된 자식해들(offsprings)을 이용하여 기존 해집단(population)의 해를 대치하여 새로운 해집단을 return
        """
        세대형 유전 알고리즘 사용
        해집단 내에서 가장 품질이 낮은 해를 대치하는 방법 사용(엘리티즘)
        """
        result_population = []
        for i in range(self.params["NUM_OFFSPRING"]):
            population.pop()
        for i in range(self.params["NUM_OFFSPRING"]):
            population.append([offsprings[i],self.get_fitness(offsprings[i])])
        result_population=population[:]
        return result_population

    # 해 탐색(GA) 함수
    def search(self):
        generation = 0  # 현재 세대 수
        population = [] # 해집단
        offsprings = [] # 자식해집단
        chromosome=""
        
        # 1. 초기화: 랜덤하게 해를 초기화
        for i in range(self.params["POP_SIZE"]):
            # todo: random 모듈을 사용하여 랜덤한 해 생성, self.params["range"]를 사용할 것
            # todo: fitness를 구하는 함수인 self.get_fitness()를 만들어서 fitness를 구할 것
            # todo: 정렬함수인 self.sort_population()을 사용하여 population을 정렬할 것            
            for j in range(self.params["RANGE"]):
                gene=random.randint(0, 1)
                chromosome=chromosome+str(gene)
            fitness=self.get_fitness(chromosome)
            population.append([chromosome,fitness])
            chromosome=""
        self.sort_population(population)
        print("initialzed population : \n", population, "\n\n")
        
        while 1:
            offsprings = []
            count_end=0 #동일 갯수
            for i in range(self.params["NUM_OFFSPRING"]):
                #offsprings = []                 
                # 2. 선택 연산
                mom_ch, dad_ch = self.selection_operater(population)

                # 3. 교차 연산
                offspring = self.crossover_operater(mom_ch, dad_ch)
                
                # 4. 변이 연산
                # todo: 변이 연산여부를 결정, self.params["MUT"]에 따라 변이가 결정되지 않으면 변이연산 수행하지 않음
                mute_development=random.uniform(0,100)
                if mute_development<self.params["MUT"]:
                    offspring = self.mutation_operater(offspring)
                offsprings.append(offspring)
            # 5. 대치 연산
            population = self.replacement_operator(population, offsprings)
            self.sort_population(population)
            self.print_average_fitness(population) # population의 평균 fitness를 출력함으로써 수렴하는 모습을 보기 위한 기능
            generation=generation+1
            # 6. 알고리즘 종료 조건 판단
            # todo population이 전체 중 self.params["END"]의 비율만큼 동일한 해를 갖는다면 수렴했다고 판단하고 탐색 종료
            for i in range(self.params["POP_SIZE"]):
                if population[0][1]==population[i][1]:
                    count_end=count_end+1
            if count_end/self.params["POP_SIZE"]>=self.params["END"]:
                print(population)
                print(count_end/self.params["POP_SIZE"])
                print(count_end)
                break

        # 최종적으로 얼마나 소요되었는지의 세대수, 수렴된 chromosome과 fitness를 출력
        print("탐색이 완료되었습니다. \t 최종 세대수: {},\t 최종 해: {},\t 최종 적합도: {}".format(generation, population[0][0], population[0][1]))


if __name__ == "__main__":
    ga = GA(params)
    ga.search()
"""
남은 과업: 알고리즘 종료 조건 판단하기, 선택연산, 해집단 정렬 
"""

