#!/bin/bash

usage() { echo "${error} Usage: $0 -u username -a path/to/ca-certs [-p password] [-d days]" 1>&2; exit 1; }


while getopts ":u:a:" o; do
    case "${o}" in
	u)
	    username=${OPTARG}
	    ;;
	a)	    
	    capath=${OPTARG}
	    ;;
	p)
	    password=${OPTARG}    
	    ;;
	d)
	    days=${OPTARG}
	    ;;
	*)
	    usage
	    ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${username}" ] || [ -z "${capath}" ]; then
    usage
fi

[ ! -z "${password}" ] || password="xxxx"
[ ! -z "${days}" ] || days="365"

echo ${username}
echo ${capath}
echo ${password}
echo ${days}

openssl genrsa -aes256 -passout pass:${password} -out ${username}.pass.key 4096
openssl rsa -passin pass:${password} -in ${username}.pass.key -out ${username}.key

rm ${username}.pass.key

echo "${username}.key created"

openssl req -new -key ${username}.key -out ${username}.csr -subj "/C=DE/ST=Saxony/L=Leipzig/O=LeTex/CN=${username}"
openssl x509 -req -days ${days} -in ${username}.csr -CA ${capath}/ca.pem -CAkey ${capath}/ca.key -CAcreateserial -out ${username}.pem
echo "${username}.pem created"

cat ${username}.key ${username}.pem ${capath}/ca.pem > ${username}.full.pem
echo "${username}.full.pem created"

openssl pkcs12 -export -passout pass:${password} -out ${username}.full.pfx -inkey ${username}.key -in ${username}.pem -certfile ${capath}/ca.pem
echo "${username}.full.pfx created"
