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

	var barisAwal []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		barisAwal = append(barisAwal, scanner.Text())
	}

	var hasil []string
	for _, url := range barisAwal {
		lower := strings.ToLower(url)
		skip := false
		for _, filter := range kataFilter {
			if strings.Contains(lower, filter) {
				skip = true
				break
			}
		}
		if !skip {
			hasil = append(hasil, url)
		}
	}

	outputFile := strings.TrimSuffix(namaFile, filepath.Ext(namaFile)) + "_cleaned.txt"
	out, err := os.Create(outputFile)
	if err != nil {
		fmt.Println("❌ Gagal membuat file output:", err)
		return
	}
	defer out.Close()

	for _, line := range hasil {
		out.WriteString(line + "\n")
	}

	fmt.Printf("✅ %d URL dibuang. Hasil disimpan di: %s\n", len(barisAwal)-len(hasil), outputFile)
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