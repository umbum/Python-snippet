## 파일 설명
| 파일명 | 파일 용도 | 관련 절 | 페이지 |
|:--   |:--      |:--    |:--      |
| batch_norm_gradient_check.py | 배치 정규화를 구현한 신경망의 오차역전파법 방식의 기울기 계산이 정확한지 확인합니다(기울기 확인). |  |  |
| batch_norm_test.py | MNIST 데이터셋 학습에 배치 정규화를 적용해봅니다. | 6.3.2 배치 정규화의 효과 | 212 |
| hyperparameter_optimization.py | 무작위로 추출한 값부터 시작하여 두 하이퍼파라미터(가중치 감소 계수, 학습률)를 최적화해봅니다. | 6.5.3 하이퍼파라미터 최적화 구현하기 | 224 |
| optimizer_compare_mnist.py | SGD, 모멘텀, AdaGrad, Adam의 학습 속도를 비교합니다. | 6.1.8 MNIST 데이터셋으로 본 갱신 방법 비교 | 201 |
| optimizer_compare_naive.py | SGD, 모멘텀, AdaGrad, Adam의 학습 패턴을 비교합니다. | 6.1.7 어느 갱신 방법을 이용할 것인가? | 200 |
| overfit_dropout.py | 일부러 오버피팅을 일으킨 후 드롭아웃(dropout)의 효과를 관찰합니다. | 6.4.3 드롭아웃 | 219 |
| overfit_weight_decay.py | 일부러 오버피팅을 일으킨 후 가중치 감소(weight_decay)의 효과를 관찰합니다. | 6.4.1 오버피팅 | 215 |
| weight_init_activation_histogram.py | 활성화 함수로 시그모이드 함수를 사용하는 5층 신경망에 무작위로 생성한 입력 데이터를 흘리며 각 층의 활성화값 분포를 히스토그램으로 그려봅니다. | 6.2.2 은닉층의 활성화값 분포 | 203 |
| weight_init_compare.py | 가중치 초깃값(std=0.01, He, Xavier)에 따른 학습 속도를 비교합니다. | 6.2.4 MNIST 데이터셋으로 본 가중치 초깃값 비교 | 209 |
