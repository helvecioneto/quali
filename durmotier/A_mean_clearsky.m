%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% PROGRAMA PRICIPAL PARA O CALCULO DO CLEARSKY BASEADO NO METODO DE DUMORTIER 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clc;
clear;
close all;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% DIRETORIO ONDE ESTA LOCALIZADO AS COORDENADAS DAS ESTAÇOES %%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
cd '/Models/DATA/GLOBAL_GFS/use_program/'
[coordenadas,estacoes] = xlsread('BRASIL_Lon_Lat.xlsx','Plan1');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% LACO COM A QUANTIDATE DE ESTACOES A SEREM UTILIZADAS PARA O CALCULO DO CLEARSKY
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for a= 1 : length(coordenadas(:,1))  
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % PEGANDO A LATITUDE, LONGITUDE E ALTITUDE DAS ESTACOES UMA POR VEZ %%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
    latitude  = coordenadas(a,1);
    longitude = coordenadas(a,2);
    altitude  = coordenadas(a,6);
    estacao   = estacoes(a+1,3)
    ID        = estacoes(a+1,5);
    ano       = 2015:2016;
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % PROCESSAMENTO DAS IMAGENS DO LINK TURBIDITY %%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    cd '/Models/DATA/GLOBAL_GFS/use_program/use/03/Dumortier/'
    turbidity = A_F_processamento_imagens_turbidity_corrected(longitude, latitude);
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    for b = 1 : length(ano)
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % CALCULO DO CLEARSKY %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        cd '/Models/DATA/GLOBAL_GFS/use_program/use/03/Dumortier/'
        [clear_sky_hora] = A_F_clearsky_dumortier_corrected_hora(ano(1,b), longitude, latitude, altitude, turbidity);
        %[clear_sky_minute clear_sky_hora] = A_F_clearsky_dumortier_corrected(ano(1,b), longitude, latitude, altitude, turbidity);
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %clear_sky_minute_total{b} = clear_sky_minute;
        clear_sky_hora_total{b} = clear_sky_hora;
        clear clear_sky_minute clear_sky_hora;
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    end
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % SALVANDO O ARQUIVO CLEAR_SKY A CADA UMA HORA EM UM ARQUIVO .DAT %%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %clear_sky_minute = cat(1,clear_sky_minute_total{1,1},clear_sky_minute_total{1,2});
    clear_sky_hora   = cat(1,clear_sky_hora_total{1,1},clear_sky_hora_total{1,2});
    %     clear_sky_hora1  = cat(1,clear_sky_hora_total{1,1},clear_sky_hora_total{1,2});
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %     tmp1 = cat(1,0,clear_sky_hora1(:,6));
    %     tmp2 = cat(1,0,clear_sky_hora1(:,7));
    %     tmp3 = cat(1,0,clear_sky_hora1(:,8));
    %     tmp4 = cat(1,0,clear_sky_hora1(:,9));
    %     clear_sky_hora = [clear_sky_hora1(:,1:5)  tmp1(1:end-1,:) tmp2(1:end-1,:) tmp3(1:end-1,:) tmp4(1:end-1,:)];
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    cd '/Models/DATA/GLOBAL_GFS/use_program/use/03/Dumortier/ClearSky/'
    [m,k] = size(clear_sky_hora);
    arquivo = strcat(char(ID),'_hora.dat');
    fid = fopen(arquivo,'w');
    for i=1 : m
        fprintf(fid,'%4.0f  %2.0f  %2.0f  %3.0f  %2.0f  %8.2f %8.2f %8.2f %8.2f \n', clear_sky_hora(i,1), clear_sky_hora(i,2), clear_sky_hora(i,3), clear_sky_hora(i,4), clear_sky_hora(i,5), clear_sky_hora(i,6), clear_sky_hora(i,7), clear_sky_hora(i,8), clear_sky_hora(i,9));
    end
    fclose(fid);
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %[m,k] = size(clear_sky_minute);
    %arquivo = strcat(char(ID),'_minuto.dat');
    %fid = fopen(arquivo,'w');
    %for i=1 : m
    %    fprintf(fid,'%4.0f  %2.0f  %2.0f  %3.0f  %2.0f  %8.2f %8.2f %8.2f %8.2f \n', clear_sky_minute(i,1), clear_sky_minute(i,2), clear_sky_minute(i,3), clear_sky_minute(i,4), clear_sky_minute(i,5), clear_sky_minute(i,6), clear_sky_minute(i,7), clear_sky_minute(i,8), clear_sky_minute(i,9));
    %end
    %fclose(fid);
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% FIM DO PROGRAMA %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%