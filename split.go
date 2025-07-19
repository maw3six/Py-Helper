package main

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

const (
	maxFileSize = 2 * 1024 * 1024 // 2MB
)

func isDomainID(url string) bool {
	url = strings.ToLower(url)
	return strings.Contains(url, ".id")
}

func splitDomainID(fileInput string) {
	file, err := os.Open(fileInput)
	if err != nil {
		fmt.Println("❌ Gagal membuka file:", err)
		return
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	var buffer []string

	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" || !isDomainID(line) {
			continue
		}
		buffer = append(buffer, line)
	}

	if len(buffer) == 0 {
		fmt.Println("❌ Tidak ada domain .id ditemukan.")
		return
	}

	// Simpan per 2MB
	fileCount := 1
	var currentSize int
	var currentLines []string

	for _, line := range buffer {
		size := len(line) + 1 // +1 for newline
		if currentSize+size > maxFileSize {
			writeChunk(fileInput, currentLines, fileCount)
			fileCount++
			currentSize = 0
			currentLines = nil
		}
		currentLines = append(currentLines, line)
		currentSize += size
	}

	// Tulis sisa terakhir
	if len(currentLines) > 0 {
		writeChunk(fileInput, currentLines, fileCount)
	}

	fmt.Printf("✅ %d file dibuat, masing-masing maksimal 2MB.\n", fileCount)
}

func writeChunk(originalFile string, lines []string, count int) {
	outName := fmt.Sprintf("dom_id_%d.txt", count)
	outFile, err := os.Create(outName)
	if err != nil {
		fmt.Println("❌ Gagal membuat file:", outName)
		return
	}
	defer outFile.Close()

	for _, line := range lines {
		outFile.WriteString(line + "\n")
	}
	fmt.Println("✔️  File dibuat:", outName)
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

	splitDomainID(namaFile)
}