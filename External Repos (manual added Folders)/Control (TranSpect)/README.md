# control
Subversion browser for transpect based on BaseX

# install
1. clone basex-svn-api module
```bash
git clone https://github.com/transpect/basex-svn-api.git
```
2. copy lib and jar files to BaseX `custom` directory.
```bash
cp basex-svn-api/jar/basex-svn-api.jar $(BaseX)/lib/custom
cp basex-svn-api/lib/* $(BaseX)/lib/custom
```
3. clone control
```bash
git clone https://github.com/transpect/control.git
```
4. copy `control` directory in your BaseX `webapp` directory.
```bash
cp -r control $(BaseX)/webapp/
```
5. Start BaseX service
6. Open control in your browser and pass your Subversion repository URL.

http://localhost:8984/control?svnurl=https://mysvnrepo
