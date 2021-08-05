# sra-parser

### TODO

- [x]  다운로드 효율을 위해서 다운로드가 끝나면 다음 파일 다운받도록 수정 필요(현재는 한 파일당 5분 fix 상태)

# Requirement

- Docker
- SRR_Acc_list.txt
    - in SRR runner

# Usage

1. 현재 디렉토리에 엔터로 구분된 다운받고자 하는 `SRR_Acc_List.txt`가 있어야 함. 
    1. 한줄에 한 SRR, ERR 넘버가 있는 파일
2. 아래 명령어 실행
```bash
docker run --rm \
    -v $PWD:/home:rw -v $PWD/data:/home/data:rw \
    ghcr.io/williamjeong2/sra-parser:main \
    --file SRR_Acc_List.txt \
    --out data/
```

3. 다운받고 있는 파일이 화면에 출력되며 다운이 완료되면 프로그램이 종료됨.
4. 다운받은 SRA 파일들은 `/data` 디렉토리에서 확인 가능.
