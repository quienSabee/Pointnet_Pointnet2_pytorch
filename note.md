# data_loader (s3dis)
seleziona a caso un punto come centro
prende i punti in una colonna block_size * block_size centrata in tale punto
campiona num_points punti tra questi

current_points[:, 0/1] = punti traslati di - center => [-0.5, 0.5]
current_points[:, 2] = punto non traslato
current_points[:, 3/4/5] = r/g/b [0, 1]
current_points[:, 6/7/8] = questi punti scalati per le dimensioni della room [0, 1]

# modifiche
