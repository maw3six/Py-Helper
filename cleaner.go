package main

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

var kataFilter = []string{
	"cpanel", "webdisk", "webmail", "mail.", "email.", "whm",
	"autodiscover", "autoconfig", "cpcalendars", "cpcontacts",
	"smtp.", "imap.", "pop.",
	":2083", ":2087", ":2096", ":2095",
}

func bersihkanURL(namaFile string) {
	file, err := os.Open(namaFile)
	if err != nil {
		fmt.Println("❌ File tidak ditemukan:", namaFile)
		return
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	seen := make(map[string]bool)
	var hasil []string
	total := 0

	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		lower := strings.ToLower(line)
		total++

		// Skip jika mengandung kata terlarang
		skip := false
		for _, kata := range kataFilter {
			if strings.Contains(lower, kata) {
				skip = true
				break
			}
		}
		if skip || line == "" || seen[line] {
			continue
		}

		// Simpan jika belum pernah muncul
		seen[line] = true
		hasil = append(hasil, line)
	}

	outputFile := strings.TrimSuffix(namaFile, filepath.Ext(namaFile)) + "_cleaned.txt"
	out, err := os.Create(outputFile)
	if err != nil {
		fmt.Println("❌ Gagal membuat file output:", err)
		return
	}
	defer out.Close()

	for _, url := range hasil {
		out.WriteString(url + "\n")
	}

	fmt.Printf("✅ %d URL dibuang. %d URL unik disimpan di: %s\n", total-len(hasil), len(hasil), outputFile)
}

func main() {
	fmt.Println("📂 Seret file .txt ke sini atau ketik nama file:")
	var namaFile string
	fmt.Print(">> ")
	fmt.Scanln(&namaFile)

	namaFile = strings.Trim(namaFile, "\"")
	if namaFile == "" {
		fmt.Println("❌ Tidak ada input file.")
		return
	}

	bersihkanURL(namaFile)
}