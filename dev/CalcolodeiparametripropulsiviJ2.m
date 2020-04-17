close all
clear all
clc
%% Calcolo dei parametri propulsivi per il motore J-2 degli stadi S-II e S-IVB del lanciatore Saturn V %%

%% Dati raccolti
Pcc=5.26*1e6;        %Pa         Pressione in camera di combustione 
Tcc=3449.82;         %K          Temperatura in camera di combustione
r=5;                 %           Mixture ratio
tb_SII=367;          %s          Tempo di combustione per il secondo stadio
tb_SIVB1=156;        %s          Tempo di combustione per il terzo stadio alla prima accensione
tb_SIVB2=336;        %s          Tempo di combustione per il terzo stadio alla seconda accensione
MmOx=31.988;         %kg/kmol    Massa molare dell'ossidante (LOx)
MmH2=2.016;          %kg/kmol    Massa molare del combustibile (LH2)
Mmgc=8.9;            %kg/kmol    Massa molare dei gas combusti
gammagc=1.26;        %           Indice politropica
TcOx=54.36;          %K          Temperatura di congelamento di Ox
TcH2=14;             %K          Temperatura di congelamento di H2
TeOx=90.19;          %K          Temperatura di ebollizione di Ox
TeH2=20.27;          %K          Temperatura di ebollizione di H2
epsilon=27.5;        %           Rapporto tra l'area di efflusso con l'area di gola
R=8314.5;            %J/(kg*K)   Costante universale dei gas perfetti
R2=287;              %m^2/(K*s^2)                "
MOx_SII=356182/5;    %kg         Massa di Ox per il secondo stadio
MH2_SII=68260/5;     %kg         Massa di H2 per il secondo stadio
MOx_SIVB=86229.3;    %kg         Massa di Ox per il terzo stadio
MH2_SIVB=17477.4;    %kg         Massa di H2 per il terzo stadio
go=9.81;             %m/s^2      Accelerazione di gravità a quota zero (sea level)
a=0.0065;            %K/m        Gradiente verticale di temperatura
Po=101325;           %Pa         Pressione a quota zero
To=288.16;           %K          Temperatura a quota zero
z=linspace(0,200000,0.1);  %m    Quota

%% Risoluzione
Pamb=@(z) Po*(1-a*z/To)^(go/(R2*a))     %Pa       Pressione ambiente in funzione della quota
G=@(Pe) (((gammagc+1)/2)^(1/(gammagc-1)))*sqrt((gammagc+1)/(gammagc-1))*((Pe/Pcc)^(1/gammagc))*sqrt(1-(Pe/Pcc)^((gammagc-1)/gammagc))-(1/epsilon);
Pe=fzero(G,30000)                        %Pa       Pressione all'efflussso

Rgc=R/Mmgc
GAMMA=sqrt(gammagc*(2/(gammagc+1))^((gammagc+1)/(gammagc-1)))
vc=sqrt(Rgc*Tcc)/GAMMA                                                                                           %m/s         Velocità caratteristica (c*)                                                                                               
cf=@(Pamb) sqrt((2*(gammagc^2)/(gammagc-1))*((2/(gammagc+1))^((gammagc+1)/(gammagc-1))))+epsilon*((Pe-Pamb)/Pcc)  %            Coefficente di spinta
Ve=sqrt((2*gammagc/(gammagc-1))*Rgc*Tcc*(1-(Pe/Pcc)^((gammagc-1)/gammagc)))                                       %m/s         Velocità di effllusso

Mtot_SII=MOx_SII+MH2_SII                        %kg        Massa totale di propellente per il secondo stadio
mtot_SII=Mtot_SII/tb_SII                        %kg/s      Portata di propellente del secondo stadio
Fmax_SII=mtot_SII*Ve                            %N         Spinta nella condizione di ottimo del secondo stadio
Is_SII=Fmax_SII/(mtot_SII*go)                   %s         Impulso specifico nella condizione di ottimo del secondo stadio

Mtot_SIVB=MOx_SIVB+MH2_SIVB                     %kg        Massa totale di propellente per il terzo stadio
mtot_SIVB=Mtot_SIVB/(tb_SIVB1+tb_SIVB2)         %kg/s      Portata di propellente del terzo stadio
Fmax_SIVB=mtot_SIVB*Ve                          %N         Spinta nella condizione di ottimo del terzo stadio
Is_SIVB=Fmax_SIVB/(mtot_SIVB*go)                %s         Impulso specifico nella condizione di ottimo del terzo stadio

F_SII=@(Pamb) mtot_SII*Ve+(Pe-Pamb)*(epsilon*Ag);    %N.B. Manca da trovare Ag --> altra ese!!!
Is_SII=@(Pamb) F_SII/(mtot_SII*go);
F_SIVB=@(Pamb) mtot_SIVB*Ve+(Pe-Pamb)*(epsilon*Ag);  %N.B. Manca da trovare Ag --> altra ese!!!
Is_SIVB=@(Pamb) F_SIVB/(mtot_SIVB*go);
% Scrivere F, cf e Is in funzione di z?
% Scrivere z in funzione di t? (forse Tsiolkowski? facendo la derivata?)
% Scrivere F, cf e Is in funzione di t? 

%% Tsiolkowski
%N.B. MR varia nel tempo fino a circa 2 min e 30 sec MR=5.0 poi shifta a
%MR=5.5 fino a circa 7 min e 20 sec e infine shifta a MR=4.5
%N.B. Anche Is è variabile!!!
%dU=-go*Is*log(MR);


