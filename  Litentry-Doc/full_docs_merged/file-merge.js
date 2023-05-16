let fs = require('fs');
let path = require('path');

let source_path = `C:\\Users\\byj\\Documents\\Web3Go\\projects\\web3go-network-data-collection-agent\\ Litentry-Doc\\crawler_chinese`;

let target_file_path =`C:\\Users\\byj\\Documents\\Web3Go\\projects\\web3go-network-data-collection-agent\\ Litentry-Doc\\full_docs_merged\\Litentry`
// let target_file =`${target_file_path}\\Litentry-Doc-en.txt`;
let target_file =`${target_file_path}\\Litentry-Doc-zh-Hans.txt`;
function walkPathSync(currentDirPath, callback) {
    fs.readdirSync(currentDirPath, { withFileTypes: true }).forEach(function (dirent) {
        var filePath = path.join(currentDirPath, dirent.name);
        if (dirent.isFile()) {
            callback(filePath, dirent);
        } else if (dirent.isDirectory()) {
            walkSync(filePath, callback);
        }
    });
}
let all_texts = [];
walkPathSync(source_path, function (filePath, stat) {
    console.log(filePath);
    let text = fs.readFileSync(filePath).toString()
    all_texts.push(text)
});


fs.writeFileSync(target_file, all_texts.join('\n\n'))