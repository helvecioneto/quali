function [clear_sky_minute clear_sky_hora] = clearsky_dumortier(ano, longitude, latitude, altitude, turbidity)
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Ls É A LONGITUDE PADRAO PARA O BRASIL É DE -45. SE QUISER USAR UTC, Ls = 0 %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    Ls = 0;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % SERA CALCULADO SE O ANO É BISSEXTO E QUANTAS HORAS E MINUTOS EXISTEM EM UM ANO %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    day_year = yeardays(ano);
    day = 1:day_year;
    hour_year = day_year*24;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % QUANTOS MINUTOS E HORAS EXISTEM EM UM ANO %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    l=1;
    z=1;
    for i = 1:day_year
        for j = 1:1440
            minute(l) = j;
            l = l + 1;
        end
        for w = 1 : 24
            hora(z) = w;
            z = z + 1;
        end
    end
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % FAZENDO O CABECARIO PARA A COLUNA DO ANO %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    l=1;
    z=1;
    for i = 1:day_year
        for j = 1:1440
            ano_minute(l) = ano;
            l = l + 1;
        end
        for w = 1 : 24
            ano_hora(z) = ano;
            z = z + 1;
        end
    end
                    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % AJUSTE DO DIA JULIANO PARA O ANO EM QUESTAO EM MINUTOS OU HORAS %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    l=1;
    z=1;
    for i = 1:day_year
        for j = 1:1440
            day_jul_minute(l) = day(i);
            l = l + 1;
        end
        for w = 1 : 24
            day_jul_hora(z) = day(i);
            z = z + 1;
        end
    end
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % CALCULO DOS MESES COM BASE NO DIA JULIANO PARA CADA MINUTO %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    for t = 1:day_jul_minute(end)*1440
        if(day_year == 366) 
                if (day_jul_minute(t) <= 31)
                    mounth_minute(t) = 1;
                elseif ((day_jul_minute(t) > 31) && (day_jul_minute(t) <= 60))
                    mounth_minute(t) = 2;
                elseif ((day_jul_minute(t) > 60) && (day_jul_minute(t) <= 91))
                    mounth_minute(t) = 3;
                elseif ((day_jul_minute(t) > 91) && (day_jul_minute(t) <= 121))
                    mounth_minute(t) = 4;
                elseif ((day_jul_minute(t) > 121) && (day_jul_minute(t) <= 152))
                    mounth_minute(t) = 5;
                elseif ((day_jul_minute(t) > 152) && (day_jul_minute(t) <= 182))
                    mounth_minute(t) = 6;
                elseif ((day_jul_minute(t) > 182) && (day_jul_minute(t) <= 213))
                    mounth_minute(t) = 7;
                elseif ((day_jul_minute(t) > 213) && (day_jul_minute(t) <= 244))
                    mounth_minute(t) = 8;
                elseif ((day_jul_minute(t) > 244) && (day_jul_minute(t) <= 274))
                    mounth_minute(t) = 9;
                elseif ((day_jul_minute(t) > 274) && (day_jul_minute(t) <= 305))
                    mounth_minute(t) = 10;
                elseif ((day_jul_minute(t) > 305) && (day_jul_minute(t) <= 335))
                    mounth_minute(t) = 11;
                elseif ((day_jul_minute(t) > 335) && (day_jul_minute(t) <= 366))
                    mounth_minute(t) = 12;
                end
        else
                if (day_jul_minute(t) <= 31)
                    mounth_minute(t) = 1;
                elseif ((day_jul_minute(t) > 31) && (day_jul_minute(t) <= 59))
                    mounth_minute(t) = 2;
                elseif ((day_jul_minute(t) > 59) && (day_jul_minute(t) <= 90))
                    mounth_minute(t) = 3;
                elseif ((day_jul_minute(t) > 90) && (day_jul_minute(t) <= 120))
                    mounth_minute(t) = 4;
                elseif ((day_jul_minute(t) > 120) && (day_jul_minute(t) <= 151))
                    mounth_minute(t) = 5;
                elseif ((day_jul_minute(t) > 151) && (day_jul_minute(t) <= 181))
                    mounth_minute(t) = 6;
                elseif ((day_jul_minute(t) > 181) && (day_jul_minute(t) <= 212))
                    mounth_minute(t) = 7;
                elseif ((day_jul_minute(t) > 212) && (day_jul_minute(t) <= 243))
                    mounth_minute(t) = 8;
                elseif ((day_jul_minute(t) > 243) && (day_jul_minute(t) <= 273))
                    mounth_minute(t) = 9;
                elseif ((day_jul_minute(t) > 273) && (day_jul_minute(t) <= 304))
                    mounth_minute(t) = 10;
                elseif ((day_jul_minute(t) > 304) && (day_jul_minute(t) <= 334))
                    mounth_minute(t) = 11;
                elseif ((day_jul_minute(t) > 334) && (day_jul_minute(t) <= 365))
                    mounth_minute(t) = 12;
                end
        end
    end
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % CALCULO DOS MESES COM BASE NO DIA JULIANO PARA CADA HORA %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    for t = 1:day_jul_hora(end)*24
        if(day_year == 366) 
                if (day_jul_hora(t) <= 31)
                    mounth_hora(t) = 1;
                elseif ((day_jul_hora(t) > 31) && (day_jul_hora(t) <= 60))
                    mounth_hora(t) = 2;
                elseif ((day_jul_hora(t) > 60) && (day_jul_hora(t) <= 91))
                    mounth_hora(t) = 3;
                elseif ((day_jul_hora(t) > 91) && (day_jul_hora(t) <= 121))
                    mounth_hora(t) = 4;
                elseif ((day_jul_hora(t) > 121) && (day_jul_hora(t) <= 152))
                    mounth_hora(t) = 5;
                elseif ((day_jul_hora(t) > 152) && (day_jul_hora(t) <= 182))
                    mounth_hora(t) = 6;
                elseif ((day_jul_hora(t) > 182) && (day_jul_hora(t) <= 213))
                    mounth_hora(t) = 7;
                elseif ((day_jul_hora(t) > 213) && (day_jul_hora(t) <= 244))
                    mounth_hora(t) = 8;
                elseif ((day_jul_hora(t) > 244) && (day_jul_hora(t) <= 274))
                    mounth_hora(t) = 9;
                elseif ((day_jul_hora(t) > 274) && (day_jul_hora(t) <= 305))
                    mounth_hora(t) = 10;
                elseif ((day_jul_hora(t) > 305) && (day_jul_hora(t) <= 335))
                    mounth_hora(t) = 11;
                elseif ((day_jul_hora(t) > 335) && (day_jul_hora(t) <= 366))
                    mounth_hora(t) = 12;
                end
        else
                if (day_jul_hora(t) <= 31)
                    mounth_hora(t) = 1;
                elseif ((day_jul_hora(t) > 31) && (day_jul_hora(t) <= 59))
                    mounth_hora(t) = 2;
                elseif ((day_jul_hora(t) > 59) && (day_jul_hora(t) <= 90))
                    mounth_hora(t) = 3;
                elseif ((day_jul_hora(t) > 90) && (day_jul_hora(t) <= 120))
                    mounth_hora(t) = 4;
                elseif ((day_jul_hora(t) > 120) && (day_jul_hora(t) <= 151))
                    mounth_hora(t) = 5;
                elseif ((day_jul_hora(t) > 151) && (day_jul_hora(t) <= 181))
                    mounth_hora(t) = 6;
                elseif ((day_jul_hora(t) > 181) && (day_jul_hora(t) <= 212))
                    mounth_hora(t) = 7;
                elseif ((day_jul_hora(t) > 212) && (day_jul_hora(t) <= 243))
                    mounth_hora(t) = 8;
                elseif ((day_jul_hora(t) > 243) && (day_jul_hora(t) <= 273))
                    mounth_hora(t) = 9;
                elseif ((day_jul_hora(t) > 273) && (day_jul_hora(t) <= 304))
                    mounth_hora(t) = 10;
                elseif ((day_jul_hora(t) > 304) && (day_jul_hora(t) <= 334))
                    mounth_hora(t) = 11;
                elseif ((day_jul_hora(t) > 334) && (day_jul_hora(t) <= 365))
                    mounth_hora(t) = 12;
                end
        end
    end
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % CALCULO DOS DIAS COM BASE NOS MESES PARA CADA MINUTO E HORA %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    for t = 1:day_jul_minute(end)*1440
        if(day_year == 366)
            if (mounth_minute(t) == 1)
                dia_minute(t) = day_jul_minute(t);
            elseif (mounth_minute(t) == 2)
                dia_minute(t) = (day_jul_minute(t) - 31);
            elseif (mounth_minute(t) == 3)
                dia_minute(t) = (day_jul_minute(t) - 60);
            elseif (mounth_minute(t) == 4)
                dia_minute(t) = (day_jul_minute(t) - 91);
            elseif (mounth_minute(t) == 5)
                dia_minute(t) = (day_jul_minute(t) - 121);
            elseif (mounth_minute(t) == 6)
                dia_minute(t) = (day_jul_minute(t) - 152);
            elseif (mounth_minute(t) == 7)
                dia_minute(t) = (day_jul_minute(t) - 182);
            elseif (mounth_minute(t) == 8)
                dia_minute(t) = (day_jul_minute(t) - 213);
            elseif (mounth_minute(t) == 9)
                dia_minute(t) = (day_jul_minute(t) - 244);
            elseif (mounth_minute(t) == 10)
                dia_minute(t) = (day_jul_minute(t) - 274);
            elseif (mounth_minute(t) == 11)
                dia_minute(t) = (day_jul_minute(t) - 305);
            elseif (mounth_minute(t) == 12)
                dia_minute(t) = (day_jul_minute(t) - 335);
            end
        else
            if (mounth_minute(t) == 1)
                dia_minute(t) = day_jul_minute(t);
            elseif (mounth_minute(t) == 2)
                dia_minute(t) = (day_jul_minute(t) - 31);
            elseif (mounth_minute(t) == 3)
                dia_minute(t) = (day_jul_minute(t) - 59);
            elseif (mounth_minute(t) == 4)
                dia_minute(t) = (day_jul_minute(t) - 90);
            elseif (mounth_minute(t) == 5)
                dia_minute(t) = (day_jul_minute(t) - 120);
            elseif (mounth_minute(t) == 6)
                dia_minute(t) = (day_jul_minute(t) - 151);
            elseif (mounth_minute(t) == 7)
                dia_minute(t) = (day_jul_minute(t) - 181);
            elseif (mounth_minute(t) == 8)
                dia_minute(t) = (day_jul_minute(t) - 212);
            elseif (mounth_minute(t) == 9)
                dia_minute(t) = (day_jul_minute(t) - 243);
            elseif (mounth_minute(t) == 10)
                dia_minute(t) = (day_jul_minute(t) - 273);
            elseif (mounth_minute(t) == 11)
                dia_minute(t) = (day_jul_minute(t) - 304);
            elseif (mounth_minute(t) == 12)
                dia_minute(t) = (day_jul_minute(t) - 334);
            end
        end
    end
    
    for t = 1:day_jul_hora(end)*24
        if(day_year == 366)
            if (mounth_hora(t) == 1)
                dia_hora(t) = day_jul_hora(t);
            elseif (mounth_hora(t) == 2)
                dia_hora(t) = (day_jul_hora(t) - 31);
            elseif (mounth_hora(t) == 3)
                dia_hora(t) = (day_jul_hora(t) - 60);
            elseif (mounth_hora(t) == 4)
                dia_hora(t) = (day_jul_hora(t) - 91);
            elseif (mounth_hora(t) == 5)
                dia_hora(t) = (day_jul_hora(t) - 121);
            elseif (mounth_hora(t) == 6)
                dia_hora(t) = (day_jul_hora(t) - 152);
            elseif (mounth_hora(t) == 7)
                dia_hora(t) = (day_jul_hora(t) - 182);
            elseif (mounth_hora(t) == 8)
                dia_hora(t) = (day_jul_hora(t) - 213);
            elseif (mounth_hora(t) == 9)
                dia_hora(t) = (day_jul_hora(t) - 244);
            elseif (mounth_hora(t) == 10)
                dia_hora(t) = (day_jul_hora(t) - 274);
            elseif (mounth_hora(t) == 11)
                dia_hora(t) = (day_jul_hora(t) - 305);
            elseif (mounth_hora(t) == 12)
                dia_hora(t) = (day_jul_hora(t) - 335);
            end
        else
            if (mounth_hora(t) == 1)
                dia_hora(t) = day_jul_hora(t);
            elseif (mounth_hora(t) == 2)
                dia_hora(t) = (day_jul_hora(t) - 31);
            elseif (mounth_hora(t) == 3)
                dia_hora(t) = (day_jul_hora(t) - 59);
            elseif (mounth_hora(t) == 4)
                dia_hora(t) = (day_jul_hora(t) - 90);
            elseif (mounth_hora(t) == 5)
                dia_hora(t) = (day_jul_hora(t) - 120);
            elseif (mounth_hora(t) == 6)
                dia_hora(t) = (day_jul_hora(t) - 151);
            elseif (mounth_hora(t) == 7)
                dia_hora(t) = (day_jul_hora(t) - 181);
            elseif (mounth_hora(t) == 8)
                dia_hora(t) = (day_jul_hora(t) - 212);
            elseif (mounth_hora(t) == 9)
                dia_hora(t) = (day_jul_hora(t) - 243);
            elseif (mounth_hora(t) == 10)
                dia_hora(t) = (day_jul_hora(t) - 273);
            elseif (mounth_hora(t) == 11)
                dia_hora(t) = (day_jul_hora(t) - 304);
            elseif (mounth_hora(t) == 12)
                dia_hora(t) = (day_jul_hora(t) - 334);
            end
        end
    end
        
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % CALCULO DO LINK TURBIDITY PARA CADA MESES DO ANO EM MINUTO %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    for j = 1 : day_jul_minute(end)*1440
        if (mounth_minute(j) == 1)
            link_turbidity_minute(j) = turbidity(4)/20;
        elseif (mounth_minute(j) == 2)
            link_turbidity_minute(j) = turbidity(12)/20;
        elseif (mounth_minute(j) == 3)
            link_turbidity_minute(j) = turbidity(7)/20;
        elseif (mounth_minute(j) == 4)
            link_turbidity_minute(j) = turbidity(1)/20;
        elseif (mounth_minute(j) == 5)
            link_turbidity_minute(j) = turbidity(8)/20;
        elseif (mounth_minute(j) == 6)
            link_turbidity_minute(j) = turbidity(6)/20;
        elseif (mounth_minute(j) == 7)
            link_turbidity_minute(j) = turbidity(5)/20;
        elseif (mounth_minute(j) == 8)
            link_turbidity_minute(j) = turbidity(2)/20;
        elseif (mounth_minute(j) == 9)
            link_turbidity_minute(j) = turbidity(11)/20;
        elseif (mounth_minute(j) == 10)
            link_turbidity_minute(j) = turbidity(10)/20;
        elseif (mounth_minute(j) == 11)
            link_turbidity_minute(j) = turbidity(9)/20;
        elseif (mounth_minute(j) == 12)
            link_turbidity_minute(j) = turbidity(3)/20;
        end
    end  
                  
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % LACO PARA SER EFETUADO OS CALCULOS DO CLEAR SKY USANDO O METODO DE DUMORTIER %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    for t= 1 : day_jul_minute(end)*1440 
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % CALCULO DA DECLINACAO SOLAR EM RADS %
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        %day_angle(t) = ((360*(day_jul_minute(t)-1))/365)*pi/180;
        day_angle(t) = (0.017201916*day_jul_minute(t));
        dec(t) = (0.006918 - 0.399912 * cos(day_angle(t)) + 0.070257 * sin(day_angle(t)) - 0.006758 * cos(2* day_angle(t)) + 0.000907 * sin(2* day_angle(t)) - 0.002697 * cos(3* day_angle(t)) + 0.001480 * sin(3* day_angle(t)));
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % CALCULO DA EQUACAO DO TEMPO EM HORA %
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        eqtime(t) = (0.000075 + 0.001868 * cos(day_angle(t)) - 0.032077 * sin(day_angle(t)) - 0.014615 * cos(2* day_angle(t)) - 0.040849 * sin(2* day_angle(t)))*((229.18));
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % CALCULO DO TEMPO TOTAL TRANSCORRIDO OU HORA SOLAR EM MINUTO %
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
               
        tcorr(t) = (minute(t)/60 + ((longitude - Ls)/15) + eqtime(t)/60);
        
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % CALCULO DO ANGULO HORARIO EM GRAU %
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        hour_angle(t) = (12.00 - tcorr(t))* 15;
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % CALCULO DA DISTÂNCIA MÉDIA TERRA-SOL PARA CADA DIA JULIANO %
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
       
        e0(t) = 1.00011 + 0.034221 * cos(day_angle(t)) + 0.00128 * sin(day_angle(t)) + 0.000719 * cos(2 * day_angle(t)) + 0.000077 * sin(2 * day_angle(t));
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%        
        % CALCULO DO ÂNGULO ZÊNITAL, COSENO DO ANGULO ZENITAL E DO ANGULO DE ELEVAÇÃO %
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        u0(t) = ((sin(dec(t)) * sin(latitude*pi/180)) + (cos(dec(t)) * cos(latitude*pi/180) * cos(hour_angle(t)*pi/180)));
        zenit_angle(t) = (acos(u0(t)))*180/pi;
        elevation_angle(t) = (90 - zenit_angle(t));
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % CALCULO DA RADIAÇÃO SOLAR NO TOPO DA ATMOSFERA EM (W/m2) %
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        TOA(t) = 1367 * e0(t) * u0(t);
        
        if ((TOA(t)< 0))
            TOA(t) = 0;
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % CALCULO DA RELATIVE OPTICAL AIR MASS (M)%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        delta_elevation_angle(t) = ((0.061359 * (180/pi)) * (((0.1594 + ((1.1230) * (pi/180) * (elevation_angle(t)))) + (0.065656 * ((pi/180)^2) * (elevation_angle(t)^2))) / ((1 + (28.9344 * (pi/180) * elevation_angle(t))) + (277.3971 * ((pi/180)^2) * (elevation_angle(t)^2)))));
        
        true_elevation_angle(t) = elevation_angle(t) + delta_elevation_angle(t);
        
        M(t) = real((exp((-altitude)/8434.5))/(sin(true_elevation_angle(t)*(pi/180))+(0.50572*((6.07995 + true_elevation_angle(t))^-1.6364))));
              
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % CALCULO DO Aer: IS THE OPTICAL THICKNESS OF RAYLEIGH %
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        if ((M(t)<= 20))
            
            Aer(t) = ((1)/(6.6296 + 1.7513*(M(t)) - 0.1202*(M(t)^2) + 0.0065*(M(t)^3) - 0.00013*(M(t)^4)));
            
        elseif((M(t) > 20))
            
            Aer(t) = ((1)/(10.4 + (0.718*(M(t)))));
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % CALCULO DA COMPOMENTE DIRETA DA RADIAÇÂO SOLAR %
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        Ees(t) = 1367 * e0(t) * sin(elevation_angle(t)*(pi/180)) * exp(-0.8662 * link_turbidity_minute(t) * M(t) * Aer(t));
        
        if ((Ees(t)< 0))
            Ees(t) = 0;
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % CALCULO DA COMPOMENTE DIFUSSA DA RADIAÇÃO SOLAR %
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        Eed(t) = 1367 * e0(t) *  (0.0065 + (-0.045 + (0.0646 * link_turbidity_minute(t) * sin(elevation_angle(t)*(pi/180)) - (-0.014 + (0.0327 * link_turbidity_minute(t) * (sin(elevation_angle(t)*(pi/180)) * (sin(elevation_angle(t)*(pi/180)))))))));
        
        if ((Eed(t)< 0) || (Eed(t) > 1367))
            Eed(t) = 0;
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % CALCULO DA RADIAÇÃO SOLAR GLOBAL %
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        IRg(t) = Ees(t) + Eed(t);
     
    end
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % SALVANDO O CLEAR_SKY PARA CADA MINUTO DO ANO %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    clear_sky_minute(:,1) = ano_minute';
    clear_sky_minute(:,2) = mounth_minute';
    clear_sky_minute(:,3) = dia_minute';
    clear_sky_minute(:,4) = day_jul_minute';
    clear_sky_minute(:,5) = minute';
    clear_sky_minute(:,6) = TOA';
    clear_sky_minute(:,7) = Ees';
    clear_sky_minute(:,8) = Eed';
    clear_sky_minute(:,9) = IRg';
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % SALVANDO O CLEAR_SKY PARA CADA HORA DO ANO %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    clear_sky_hora(:,1) = ano_hora';
    clear_sky_hora(:,2) = mounth_hora';
    clear_sky_hora(:,3) = dia_hora';
    clear_sky_hora(:,4) = day_jul_hora';
    clear_sky_hora(:,5) = hora';
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % CALCULANDO A M�DIA PARA CADA HORA %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    zeit_ref_min = [1:+1:day_jul_minute(end)*1440]';
    starthour = [60:+60:day_jul_minute(end)*1440]';
    for s = 1:hour_year
        [zl,sl] = find(starthour(s,1) == zeit_ref_min);
        zl_min =  max(1,zl-60);
        zl_max = min(zl, day_jul_minute(end)*1440);
        TOA_media =  mean(TOA(zl_min:zl_max));                
        clear_sky_hora(s ,6) = TOA_media;
        Ees_media =  mean(Ees(zl_min:zl_max));  
        clear_sky_hora(s ,7) = Ees_media;  
        Eed_media =  mean(Eed(zl_min:zl_max));  
        clear_sky_hora(s ,8) = Eed_media; 
        IRg_media =  mean(IRg(zl_min:zl_max));  
        clear_sky_hora(s ,9) = IRg_media;
    end
end