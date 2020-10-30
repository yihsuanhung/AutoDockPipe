
AutoDock Vina Pipeline

[使用說明]
1. 更新 Ligand Database (DrugBank)
    https://www.drugbank.ca/releases/latest#structures
    下載 All structures (需登入，點擊下載或使用指令下載)
    cd drugbank/
    curl -Lfv -o drugbank_all_structures.sdf.zip -u [帳號]:[密碼] https://go.drugbank.com/releases/[版本]/downloads/all-structures
    *若無新版本則可直接跳至第5步驟

2. 將 ligands 轉成 pdbqt 格式 (使用 open babel)
    zcat drugbank_all_structures.sdf.zip | obabel -isdf --AddPolarH --append "DATABASE_ID" -opdbqt > structures.pdbqt

3. 將 ligands 切割成單一檔案
    vina_split --input structures.pdbqt
    mv structures_ligand_* ligands/

4. 將 ligands 以 100 個為單位置於不同資料夾
    qsub qsub_ligand_groups.sh

5. 準備 protein 檔案 (使用 AutoDockTools)
    此步驟需準備好 protein 的 pdbqt 檔案以及 config 檔 (config 檔可直接複製範例來改)
    從 pdb 上下載目標 protein 結構的 pdb 檔案，或使用 modeling 的方式準備好 pdb 檔案
    若 pdb 檔案中有不必要的 heteroatoms (例如 ligands, substrates)，可用記事本打開，移除所有 HETATM 開頭的 row (可使用 PyMOL 視覺化檢查)
    misc/ 裡面有 AutoDockTools 教學：
    依據 Exercise One: Preprocessing a PDB File 以及 Exercise Three: Preparing a Macromolecule 準備好 pdbqt 檔案
    依據 Exercise Four: Setting the Search Space 決定好 docking 的位置，並把以下數值貼到 protein 的 config 檔案內：
    center_x, center_y, center_z, size_x, size_y, size_z
    
6. 執行 vina 
    回到 autodock pipeline 目錄
    python qsub_vina.py -p <protein_id> (protein id 必須與 protein 內的資料夾名稱一致) 
    python qsub_vina.py -p 3pe3

7. 整理輸出結果
    qsub qsub_parser.sh (qsub 執行)
    或
    python script/parser.py (直接執行)
    輸出結果存在 result 資料夾內

8. 是視覺化輸出結果
    將 protein pdbqt 檔案以及目標 ligand pdbqt 檔案一並丟到 PyMOL 內

[Pipeline 結果]
開啟 result/ 資料夾內的 result.csv
result.csv 已將 docking 過後的 pdbqt 檔案以分數最高至最低排序
挑出前幾名的 pdbqt 檔案，在 output/ 中找到 pdbqt 檔案，即可使用 PyMOL 視覺化

[資料夾說明]
drugbank/
    存放 ligands 資料庫
protein/
    存放 protein
    第一層為 protein id 之資料夾
    第二層需包含該 protein 之 pdbqt 檔案及 config 檔案
output/
    存放 vina 與 qsub 之所有結果，包含 docking 後的 pdbqt 檔案以及 qsub 的 error 與 output 檔案
result/
    存放整理之後的輸出結果
script/
    存放 Pipeline 副程式
vina/
    存放 AutoDock Vina 主程式
