
# AutoDock Vina Pipeline
這是一個建立在台灣杉上，使用 AutoDock Vina 執行的 protein-ligand docking pipeline

## 使用說明
1. 更新 Ligand Database (DrugBank)</br>
    https://www.drugbank.ca/releases/latest#structures</br>
    下載 All structures (需登入，點擊下載或使用指令下載)</br>
    ```
    cd drugbank/
    curl -Lfv -o drugbank_all_structures.sdf.zip -u [帳號]:[密碼] https://go.drugbank.com/releases/[版本]/downloads/all-structures
    ```
    註：若無新版本則可直接跳至第5步驟

2. 將 ligands 轉成 pdbqt 格式 (使用 open babel)
    ```
    zcat drugbank_all_structures.sdf.zip | obabel -isdf --AddPolarH --append "DATABASE_ID" -opdbqt > structures.pdbqt
    ```
3. 將 ligands 切割成單一檔案
    ```
    vina_split --input structures.pdbqt
    mv structures_ligand_* ligands/
    ```
4. 將 ligands 以 100 個為單位置於不同資料夾
    ```
    qsub qsub_ligand_groups.sh
    ```
5. 準備 protein 檔案 (使用 AutoDockTools)</br>
    此步驟需準備好 protein 的 pdbqt 檔案以及 config 檔 (config 檔可直接複製範例來改)</br>
    從 pdb 上下載目標 protein 結構的 pdb 檔案，或使用 modeling 的方式準備好 pdb 檔案</br>
    若 pdb 檔案中有不必要的 heteroatoms (例如 ligands, substrates)，可用記事本打開，移除所有 HETATM 開頭的 row (可使用 PyMOL 視覺化檢查)</br>
    `misc/` 裡面有 AutoDockTools 教學：</br>
    依據 Exercise One: Preprocessing a PDB File 以及 Exercise Three: Preparing a Macromolecule 準備好 pdbqt 檔案</br>
    依據 Exercise Four: Setting the Search Space 決定好 docking 的位置，並把以下數值貼到 protein 的 config 檔案內：</br>
    center_x, center_y, center_z, size_x, size_y, size_z
    
6. 執行 vina </br>
    回到 autodock pipeline 目錄</br>
    ```
    python qsub_vina.py -p <protein_id>
    python qsub_vina.py -p 3pe3
    ```
    註：protein id 必須與 `protein/` 內的資料夾名稱一致

7. 整理輸出結果</br>
    qsub 執行
    ```
    qsub qsub_parser.sh
    ```
    或直接執行
    ```
    python script/parser.py
    ```
    輸出結果存在 `result/` 資料夾內</br>

8. 是視覺化輸出結果</br>
    將 protein pdbqt 檔案以及目標 ligand pdbqt 檔案一並丟到 PyMOL 內</br>

## Pipeline 結果
開啟 `result/` 資料夾內的 `result.csv`</br>
result.csv 已將 docking 過後的 pdbqt 檔案以分數最高至最低排序</br>
挑出前幾名的 pdbqt 檔案，在 `output/` 中找到 pdbqt 檔案，即可使用 PyMOL 視覺化</br>

## 資料夾說明
`drugbank/`</br>
    存放 ligands 資料庫</br></br>
`protein/`</br>
    存放 protein</br>
    第一層為 protein id 之資料夾</br>
    第二層需包含該 protein 之 pdbqt 檔案及 config 檔案</br></br>
`output/`</br>
    存放 vina 與 qsub 之所有結果，包含 docking 後的 pdbqt 檔案以及 qsub 的 error 與 output 檔案</br></br>
`result/`</br>
    存放整理之後的輸出結果</br></br>
`script/`</br>
    存放 Pipeline 副程式</br></br>
`vina/`</br>
    存放 AutoDock Vina 主程式</br></br>
`misc/`</br>
    存放雜項</br>
