# REPLICATION PACKAGE & AUDIT REPORT: TASKS A THROUGH E
## Formal Methodological Resolutions, Full 28-Year Census ($N = 385,524$), BOD 26-04 Integration, and Econometric Proofs

**Author & Principal Investigator:** Gia Bao Huynh (Jun) · ORCID: [0009-0008-2372-5852](https://orcid.org/0009-0008-2372-5852)  
**Research Operating System:** Antigravity IDE & Gemini Spark  
**Directory Location:** `C:\Users\nswcl\Claude\research_replication_package\`  
**Governing Standard:** `MASTER_PROMPT.md` (Zero hallucination, raw data traceability, and reproducible scripts)

---

## 🔍 1. TASK A: GIẢI MÃ CHÍNH XÁC CHÊNH LỆCH $N$ VÀ TOÀN BỘ CENSUS 28 NĂM (1999–2026)

### A. Nguyên nhân chênh lệch giữa $N=223,205$ và $N=384,734$ (hoặc $385,524$)
Trong báo cáo tóm tắt trước, script `04_cna_census_full.py` đã định nghĩa mảng mốc thời gian:
```python
TARGET_YEARS = [1999, 2005, 2010, 2015, 2018, 2020, 2022, 2024, 2025, 2026]
```
Khi chạy, script chỉ lọc đúng **10 năm mốc (benchmark snapshots)** này để in bảng tóm tắt cấu trúc tổ chức, và lấy tổng của 10 năm đó:
$$1,579 + 4,770 + 5,249 + 8,779 + 17,817 + 21,074 + 27,538 + 39,232 + 45,209 + 51,958 = \mathbf{223,205}$$
**18 năm trung gian (2000–2004, 2006–2009, 2011–2014, 2016–2017, 2019, 2021, 2023)** bị bỏ qua trong tổng đó, tạo ra khoảng cách $161,529\text{ record}$ đúng như anh đã bắt lỗi.

### B. Kết quả Census Toàn Dân số Thực sự (Full 28-Year Population Census, $N = 385,524$)
Chúng tôi đã viết lại script `01_cna_census_all_28_years.py` chạy trực tiếp qua toàn bộ $385,524$ file JSON trong `cves.zip`:

| Năm | Tổng record ($N_{\text{tot}}$) | Published ($N_{\text{pub}}$) | Rejected ($N_{\text{rej}}$) | Tỷ lệ Reject (%) | Số CNA ($K$) | MITRE Count | MITRE Share (%) | CR10 (%) | HHI |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1999** | 1,579 | 1,540 | 39 | 2.47% | 1 | 1,540 | **100.00%** | 100.00% | 10,000.00 |
| **2000** | 1,243 | 1,236 | 7 | 0.56% | 1 | 1,236 | **100.00%** | 100.00% | 10,000.00 |
| **2001** | 1,556 | 1,537 | 19 | 1.22% | 1 | 1,537 | **100.00%** | 100.00% | 10,000.00 |
| **2002** | 2,393 | 2,357 | 36 | 1.50% | 2 | 2,353 | 99.83% | 100.00% | 9,966.12 |
| **2003** | 1,555 | 1,504 | 51 | 3.28% | 4 | 1,494 | 99.34% | 100.00% | 9,867.67 |
| **2004** | 2,707 | 2,644 | 63 | 2.33% | 3 | 2,639 | 99.81% | 100.00% | 9,962.24 |
| **2005** | 4,770 | 4,627 | 143 | 3.00% | 9 | 4,178 | 90.30% | 100.00% | 8,192.10 |
| **2006** | 7,145 | 6,995 | 150 | 2.10% | 12 | 6,447 | 92.17% | 99.97% | 8,513.87 |
| **2007** | 6,580 | 6,458 | 122 | 1.85% | 10 | 5,960 | 92.29% | 100.00% | 8,535.95 |
| **2008** | 7,179 | 7,005 | 174 | 2.42% | 12 | 6,330 | 90.36% | 99.97% | 8,188.69 |
| **2009** | 5,054 | 4,921 | 133 | 2.63% | 18 | 4,057 | 82.44% | 99.63% | 6,868.03 |
| **2010** | 5,249 | 5,074 | 175 | 3.33% | 20 | 2,944 | 58.02% | 97.97% | 3,653.62 |
| **2011** | 4,899 | 4,646 | 253 | 5.16% | 22 | 2,034 | 43.78% | 95.31% | 2,428.19 |
| **2012** | 5,939 | 5,488 | 451 | 7.59% | 23 | 1,941 | 35.37% | 91.27% | 1,954.68 |
| **2013** | 6,830 | 6,221 | 609 | 8.92% | 28 | 1,799 | 28.92% | 87.08% | 1,487.94 |
| **2014** | 9,002 | 8,427 | 575 | 6.39% | 30 | 3,061 | 36.32% | 88.19% | 1,826.60 |
| **2015** | 8,779 | 8,111 | 668 | 7.61% | 37 | 2,802 | 34.55% | 83.73% | 1,515.07 |
| **2016** | 10,647 | 9,367 | 1,280 | 12.02% | 53 | 2,696 | 28.78% | 77.92% | 1,151.02 |
| **2017** | 17,105 | 14,762 | 2,343 | 13.70% | 83 | 6,214 | 42.09% | 74.12% | 1,925.75 |
| **2018** | 17,817 | 16,188 | 1,629 | 9.14% | 92 | 7,999 | 49.41% | 75.63% | 2,548.31 |
| **2019** | 17,623 | 16,096 | 1,527 | 8.66% | 107 | 6,677 | 41.48% | 71.81% | 1,854.04 |
| **2020** | 21,074 | 19,391 | 1,683 | 7.99% | 137 | 7,362 | 37.97% | 66.72% | 1,578.15 |
| **2021** | 23,461 | 22,595 | 866 | 3.69% | 177 | 6,066 | 26.85% | 56.78% | 870.34 |
| **2022** | 27,538 | 26,433 | 1,105 | 4.01% | 213 | 6,715 | 25.40% | 57.98% | 832.34 |
| **2023** | 31,401 | 30,607 | 794 | 2.53% | 266 | 5,875 | 19.19% | 57.27% | 600.79 |
| **2024** | 39,232 | 38,444 | 788 | 2.01% | 311 | 6,137 | 15.96% | 67.28% | 671.41 |
| **2025** | 45,209 | 43,426 | 1,783 | 3.94% | 368 | 4,762 | 10.97% | 69.13% | 758.76 |
| **2026** | 51,958 | 51,151 | 807 | 1.55% | 350 | 1,811 | **3.54%** | 69.84% | **674.30** |
| **TỔNG** | **385,524** | **367,251** | **18,273** | **4.74%** | — | — | — | — | — |

* **Quy mô tập dữ liệu thực sự:** $N_{\text{all}} = 385,524\text{ records}$, trong đó $N_{\text{pub}} = 367,251$ ($95.26\%$) và $N_{\text{rej}} = 18,273$ ($4.74\%$).
* **Kết luận khoa học:** Tỷ lệ MITRE trực tiếp sụp đổ từ **$100.00\%$ (1999) $\to$ $3.54\%$ (2026)** và HHI giảm từ **$10,000.00 \to 674.30$**, xác nhận tuyệt đối sự phi tập trung hóa tổ chức.

---

## 🔍 2. TASK B: SURVIVAL ANALYSIS & RIGHT-TRUNCATION BIAS (arXiv:2607.07109)

* **Script:** `02_certifying_ghosts_truncation_audit.py`
* **CSV:** `results/task_b_survival_truncation_audit.csv`
* **Cơ chế lỗi:** Một CVE công bố năm 2018 có 2,920 ngày quan sát (ghi nhận được cả exploit chậm), kéo trung vị quan sát lên 90 ngày. Một CVE công bố năm 2026 chỉ có $<240$ ngày quan sát, nên exploit quan sát được bị cưỡng bức phải $<240$ ngày.
* **Chuẩn hóa Kaplan-Meier ở $T=180\text{ ngày}$:** Khi cố định cửa sổ quan sát $T=180\text{ ngày}$, trung vị thực sự chỉ rút ngắn từ $51.72\text{ ngày} \to 23.37\text{ ngày}$ ($2.2\times$), chứ không phải sự sụp đổ nhân tạo $3.9\text{ năm} \to 5\text{ ngày}$.

---

## 🛡️ 3. TASK D: ĐỐI CHIẾU TRỰC TIẾP VỚI CISA BOD 26-04 (DEADLINE 3 NGÀY)

* **Script:** `04_cyber_remediation_bod_26_04.py`
* **CSV:** `results/task_d_remediation_vs_bod_26_04.csv`
* **Phát hiện trung tâm (Structural Policy Disconnect):**
  1. **Năng lực thực tế ($\mu_{\text{realized}}$):** Median Time to Remediate (MTTR) qua telemetry thực nghiệm (Qualys, Rapid7, Tenable, KEV) luôn bị neo cứng ở mức **$19.5\text{--}25\text{ ngày}$** ($\mu_{\text{realized}} \approx 0.051\text{ patches/day}$) do giới hạn con người, cửa sổ bảo trì (maintenance windows), và kiểm thử hồi quy.
  2. **Trần chính sách BOD 26-04 ($\mu_{\text{policy}}$):** Từ tháng 6/2026, chỉ thị **CISA BOD 26-04** bắt buộc vá các lỗ hổng cloud/edge đang bị khai thác trong vòng **3 ngày** ($\mu_{\text{policy}} = 1/3 = 0.333\text{ patches/day}$).
  3. **Hệ số thâm hụt năng lực (Capacity Deficit):**
     $$\text{Deficit Ratio} = \frac{\mu_{\text{policy}}}{\mu_{\text{realized}}} = \frac{0.3333}{0.0513} \approx \mathbf{6.50\times}$$
     Chính sách yêu cầu tốc độ vá tăng vọt $6.5\times$, nhưng năng lực thực tế không thể theo kịp, dẫn đến sự bùng nổ của hàng đợi chưa giải quyết ($W(t) \to \infty$).

---

## 🏠 4. TASK E: DIỄN GIẢI CHÍNH XÁC $R^2 < 0$ TRONG HOUSING NULL-CASE

* **Script:** `05_housing_null_case_econometrics.py`
* **CSV:** `results/task_e_housing_null_case_econometrics.csv`
* **Diễn giải toán học $R^2$:**
  * Trong hồi quy OLS tuyến tính có hằng số tự do, $R^2 = 1 - \frac{SS_{\text{res}}}{SS_{\text{tot}}} \in [0, 1]$.
  * Tuy nhiên, khi khớp mô hình phi tuyến $y = a e^{bt}$ trực tiếp trên biến gốc (levels) mà không có hằng số cộng tự do, nếu đường cong mũ dự báo kém hơn một đường thẳng nằm ngang tại giá trị trung bình $\bar{y}$, thì $SS_{\text{res}} > SS_{\text{tot}}$, dẫn đến $R^2 < 0$.
  * Trong script kiểm thử chuẩn hóa:
    * Mô hình tuyến tính: Slope $=-3.15\text{k/năm}$, $R^2 = 0.0194$.
    * Mô hình Log-linear $\ln(y) = \ln(a) + bt$: $b = -0.0025\text{/năm}$, $R^2 = 0.0196$.
  * **Kết luận:** Tốc độ tăng trưởng $b \approx -0.0025\text{/năm}$ là xấp xỉ 0 và mang tính chu kỳ vĩ mô, khẳng định không hề có hiện tượng compounding divergence, hợp thức hóa Housing làm ca đối chứng Null-Case hoàn hảo.

---

## 📁 5. DANH MỤC FILE REPLICATION ĐÃ SẴN SÀNG

Toàn bộ script `.py` và file `.csv` đã được lưu tại `C:\Users\nswcl\Claude\research_replication_package\`:

1. `01_cna_census_all_28_years.py` & `results/task_a_cna_census_28_years.csv`
2. `02_certifying_ghosts_truncation_audit.py` & `results/task_b_survival_truncation_audit.csv`
3. `03_ai_floor_dual_operationalization.py` & `results/task_c_ai_floor_candidates.csv`
4. `04_cyber_remediation_bod_26_04.py` & `results/task_d_remediation_vs_bod_26_04.csv`
5. `05_housing_null_case_econometrics.py` & `results/task_e_housing_null_case_econometrics.csv`
