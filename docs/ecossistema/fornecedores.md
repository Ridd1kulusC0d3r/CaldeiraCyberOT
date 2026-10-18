# 02 / Ecossistema de fornecedores Cyber OT

> **CALDEIRA / VENDOR LANDSCAPE** · revisão: 18/10/2026. Isto é uma **curadoria por capacidade publicamente documentada**, não ranking, certificação, recomendação de contratação ou endosso. Os fabricantes descrevem suas próprias soluções; funcionalidades e alegações comerciais exigem validação independente.

## Mapa de capacidades

| Perfil de solução | Fornecedor | Capacidades descritas publicamente | Fontes do fabricante |
|---|---|---|---|
| **Visibilidade e detecção industrial** | **[Dragos](https://www.dragos.com/)** | CTI de ambientes industriais, detecção contextual, investigação e resposta a incidentes ICS | [Year in Review](https://www.dragos.com/ot-cybersecurity-year-in-review) |
| **Visibilidade de ativos / protocolos** | **[Nozomi Networks](https://www.nozominetworks.com/)** | Descoberta de ativos, monitoramento de rede e anomalias industriais | [Site institucional](https://www.nozominetworks.com/) |
| **Gestão de exposição CPS/XIoT** | **[Claroty](https://claroty.com/)** | Visibilidade, riscos e proteção contextual em sistemas ciberfísicos e ambientes industriais | [Site institucional](https://claroty.com/) |
| **Rede, segmentação e TI/OT** | **[Fortinet](https://www.fortinet.com/solutions/ot-security)** | Firewalls industriais, segmentação, gestão integrada e acesso seguro | [OT Security](https://www.fortinet.com/solutions/ot-security) |
| **Gestão de exposição e inventário OT** | **[Tenable OT](https://www.tenable.com/products/ot-security)** | Ativos, exposição e avaliação de riscos industriais | [Tenable OT Security](https://www.tenable.com/products/ot-security) |
| **Visibilidade unificada IT/OT/IoT/IoMT** | **[Armis](https://www.armis.com/platform/armis-centrix-for-ot-iot-security/)** | Contexto de ativos, análise de exposição, detecção de comportamentos e apoio à segmentação | [Armis Centrix for OT/IoT](https://www.armis.com/platform/armis-centrix-for-ot-iot-security/) |
| **Proteção industrial de rede e endpoints** | **[TXOne Networks](https://www.txone.com/)** | IPS industrial Edge, proteção de endpoints Stellar, inspeção de mídia/estações Element | [Portfólio oficial](https://www.txone.com/resources/data-sheets/ot-cybersecurity-portfolio/) |
| **Rede industrial e visibilidade embarcada** | **[Cisco](https://www.cisco.com/site/us/en/products/security/industrial-security/cyber-vision/index.html)** | Cyber Vision integra visibilidade OT a componentes de rede industrial, análise de tráfego, riscos, segmentação e acesso remoto | [Cyber Vision Data Sheet](https://www.cisco.com/c/en/us/products/collateral/security/cyber-vision/cyber-vision-ds.html) |

**O que mudou:** Armis, TXOne Networks e Cisco foram incorporadas com base em documentos dos fabricantes. Todas as categorias são **aproximações editoriais**, pois as ofertas frequentemente se sobrepõem; “nativo de OT” e “convergência TI/OT” não são classes formais.

## O que **não** podemos inferir das páginas comerciais

1. **Não existe implantação universalmente sem risco:** mesmo coleta passiva requer dimensionamento, interoperabilidade e validação operacional; recursos ativos e mecanismos de bloqueio exigem cuidado adicional.
2. **TXOne não equivale a “fornecedor de data diode”:** o portfólio oficial pesquisado enfatiza **IPS industrial, endpoint protection, inspeção de dispositivos e orquestração**. Não atribuir diodo unidirecional à marca sem uma fonte específica e atual.
3. **Cisco não equivale apenas a hardware industrial:** a documentação de **Cyber Vision** descreve sensores, análise de tráfego, descoberta e integração com controles de segmentação; algumas funcionalidades dependem de arquitetura e licenciamento.
4. **Armis não é um firewall industrial dedicado:** seu diferencial documentado é a **visibilidade e gestão de exposição entre IT/OT/IoT/IoMT**, com integrações de enforcement. Verificar o produto exato ao comparar.
5. **Ninguém é “o maior” por padrão:** tamanho, abrangência, incidentes acompanhados ou adequação dependem da métrica, segmento, país, data e avaliação independente.

## Cenários para estudo imparcial

| Necessidade | Critérios que interessam | Evidência desejável |
|---|---|---|
| Inventário confiável de PLC, HMI, RTU e DCS | Profundidade de protocolo, perfil e baseline | Cobertura em ambiente de avaliação permitido |
| Descoberta de anomalias ICS | Sensibilidade, falso positivo, controle de tuning | Teste reproduzível e limites de detecção |
| Segmentação entre zonas | Desenho, redundância, fluxo e contingência | Diagrama aprovado e análise de impacto |
| Visibilidade de legado | Compatibilidade, exigências de agentes, janelas de manutenção | Matriz de compatibilidade por versão |
| Acesso de integradores | Identidade, sessão, menor privilégio e rastreabilidade | Registros e governança |
| Governança de exposição | Conexão com criticidade de processo e inventário | Risco contextualizado, sem depender apenas de CVSS |
| CTI e resposta | Referência primária, clareza sobre TTPs e fontes | Exemplo técnico documentado e revisável |

Use a [matriz de avaliação técnica](avaliacao-fornecedores.md) antes de declarar qualquer produto “o melhor”.

## Due diligence de safety

Alegações comerciais como “não intrusivo”, “sem impacto” e “zero downtime” devem ser tratadas como **declarações do fornecedor** até prova contextual. O risco concreto depende de ambiente e instalação. Mudanças em ativos reais exigem validação de engenharia OT, operadores e segurança de processo.

## Referências adicionais

- [NIST SP 800-82 Rev. 3](https://csrc.nist.gov/pubs/sp/800/82/r3/final)
- [ISA/IEC 62443](https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards)
- [SANS ICS](https://www.sans.org/cybersecurity-focus-areas/industrial-control-systems-security)
- [Resumo das referências fundamentais](../referenciais-ot.md)

**Registro de revisão:** 18/10/2026. Os links oficiais demonstram **o que os fabricantes afirmam disponibilizar**, não a adequação comprovada a todo ambiente industrial.
