
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

5. 執行 vina 
    回到 autodock pipeline 目錄
    python qsub_vina.py -p <protein_id> (protein id 必須與 protein 內的資料夾名稱一致) 
    python qsub_vina.py -p 3pe3

6. 整理輸出結果
    qsub qsub_parser.sh (qsub 執行)
    或
    python script/parser.py (直接執行)
    輸出結果存在 result 資料夾內

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
