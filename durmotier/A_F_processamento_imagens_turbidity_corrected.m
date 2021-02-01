function turbidity = A_F_processamento_imagens_turbidity_corrected(longitude, latitude)

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % DIRETORIO ONDE ESTA LOCALIZADO AS IMAGENS %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    cd '/Models/DATA/GLOBAL_GFS/use_program/use/03/Dumortier/IMAGENS/'
    listar_arquivos = dir('*.tif');
    n = length(listar_arquivos);

    for a= 1 : n
       cd '/Models/DATA/GLOBAL_GFS/use_program/use/03/Dumortier/IMAGENS/'
       arquivo = listar_arquivos(a) .name;
       I = imread(arquivo);
       [m,k] = size(I);
       bin_lat = 180/m;
       bin_lon = 360/k;
       lat = [90:-bin_lat:-90];
       lon = [-180:bin_lon:180];

       [linha] = find(latitude == lat);
       if isempty(linha)
            lat_lin_maior = find(lat < latitude);
            lat_val_maior = lat(lat_lin_maior);
            lat_val_maior = lat_val_maior(1);
            lat_div_maior = (lat_val_maior - (latitude));
            lat_lin_menor = find(lat > latitude);
            lat_val_menor = lat(lat_lin_menor);
            lat_val_menor = lat_val_menor(end);
            lat_div_menor = ((latitude) - lat_val_menor);
            if (lat_div_menor <= lat_div_maior)
                lat_s = lat_val_maior;
            else
                lat_s = lat_val_menor; 
            end
       else
           lat_s = lat(linha);
       end

       [coluna] = find(longitude == lon);
       if isempty(coluna)
            lon_lin_maior = find(lon < longitude);
            lon_val_maior = lon(lon_lin_maior);
            lon_val_maior = lon_val_maior(end);
            lon_div_maior = (lon_val_maior - (longitude));
            lon_lin_menor = find(lon > longitude);
            lon_val_menor = lon(lon_lin_menor);
            lon_val_menor = lon_val_menor(1);
            lon_div_menor = ((longitude) - lon_val_menor);
            if (lon_div_menor <= lon_div_maior)
                lon_s = lon_val_maior;
            else
                lon_s = lon_val_menor; 
            end
       else
           lon_s = lon(coluna);
       end

       [linha] = find(lat_s == lat);
       [coluna] = find(lon_s == lon);
       turbidity(a) = double(I(linha,coluna));
    end
end
