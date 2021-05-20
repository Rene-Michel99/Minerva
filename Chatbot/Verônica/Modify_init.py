import pickle

with open("ini.pickle","rb")as f:
    neuron1,neuron2,last_n1,last_n2,epochs = pickle.load(f)


print("Qntd de neuronios das camadas(next): ",neuron1,neuron2)
print("Qntd de neuronios das camadas(atual): ",last_n1,last_n2)
print("Numero de epochs: ",epochs)

opt = input("Qual deseja mudar? (1->neurons)(2->n_atuais)(3->epochs)")
qntd = int(input("Qual o número?"))
if opt==1:
    neuron1 = qntd
    neuron2 = qntd
elif opt==2:
    last_n1 = qntd
    last_n2 = qntd
else:
    epochs = qntd

with open("ini.pickle", "wb") as f:
    pickle.dump((neuron1,neuron2,last_n1,last_n2,epochs), f)
