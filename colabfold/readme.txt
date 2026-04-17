https://github.com/YoshitakaMo/localcolabfold

Se instaló localcolabfold para Linux siguiendo los ejcutando los siguientes comandos:

    curl -fsSL https://pixi.sh/install.sh | sh
    git clone https://github.com/yoshitakamo/localcolabfold.git
    cd localcolabfold
    pixi install && pixi run setup

Una vez instalado, se probó con que funcionara correctamente con el sample que incluye el repositorio, utilizando el siguiente comando:

    bash run_colabfoldbatch_sample.sh

Una vez comprobado el correcto funcionamiento, se colocaron las carpetas Similar y Novel dentro de la carpeta localcolabfold que fue clonada del repositorio, y se ejecutó el siguiente script de bash (run_all_colabfold.sh):

    #!/bin/bash

    echo "Starting ColabFold batch run..."

    export TF_FORCE_UNIFIED_MEMORY=1
    export XLA_PYTHON_CLIENT_MEM_FRACTION=4.0
    export TF_FORCE_GPU_ALLOW_GROWTH=true

    for f in Similar/*.fasta Novel/*.fasta; do
      name=$(basename "$f" .fasta)

      if [ ! -d "results_$name" ]; then
        echo "Running $name..."
        colabfold_batch --num-recycle 2 "$f" "results_$name"
      else
        echo "Skipping $name (already exists)"
      fi
    done

    echo "All jobs finished!"
