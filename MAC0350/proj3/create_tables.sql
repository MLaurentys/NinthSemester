-- Deletes tables, recreates them, and grant priviledges to other group member
-- uses base (given) script with few chages

DROP TABLE IF EXISTS amostra, exame, gerencia, usuario, paciente, perfil,
pertence, possui, realiza, servico, tutelamento, usuario, historico CASCADE;

CREATE TABLE IF NOT EXISTS usuario (
    id_usuario    INT NOT NULL PRIMARY KEY,
    cpf    CHAR(11) NOT NULL,
    nome    VARCHAR(255) NOT NULL,
    area_de_pesquisa    VARCHAR(255),
    instituicao    VARCHAR(255),
    data_de_nascimento    DATE,
    login    VARCHAR(255) NOT NULL,
    senha    VARCHAR(255) NOT NULL,
    id_tutor   INT references usuario(id_usuario)
);

CREATE TABLE IF NOT EXISTS perfil (
    id_perfil    INT NOT NULL PRIMARY KEY,
    codigo    VARCHAR(255) NOT NULL,
    tipo    VARCHAR(255) NOT NULL
);

--Relacionamento possui
CREATE TABLE IF NOT EXISTS possui (
    id_usuario    INT NOT NULL references usuario(id_usuario),
    id_perfil    INT NOT NULL references perfil(id_perfil)
);

CREATE TABLE IF NOT EXISTS servico (
    id_servico    INT NOT NULL PRIMARY KEY,
    nome    VARCHAR(255) NOT NULL,
    classe    VARCHAR(255) NOT NULL CHECK (classe IN ('visualização', 'inserção', 'alteração', 'remoção'))
);

--Relacionamento pertence
CREATE TABLE IF NOT EXISTS pertence (
    id_servico    INT NOT NULL references servico(id_servico),
    id_perfil    INT NOT NULL references perfil(id_perfil)
);

--Relacionamento tutelamento
CREATE TABLE IF NOT EXISTS tutelamento (
    id_usuario    INT NOT NULL references usuario(id_usuario),
    id_tutor    INT NOT NULL references usuario(id_usuario),
    id_servico    INT NOT NULL references servico(id_servico),
    id_perfil    INT NOT NULL references perfil(id_perfil),
    data_de_inicio    DATE NOT NULL,
    data_de_termino    DATE
);

CREATE TABLE IF NOT EXISTS paciente (
    id_paciente    INT NOT NULL PRIMARY KEY,
    cpf    VARCHAR(11) NOT NULL,
    nome    VARCHAR(255) NOT NULL,
    endereco    VARCHAR(255) NOT NULL,
    nascimento    DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS exame (
    id_exame    INT NOT NULL PRIMARY KEY,
    tipo    VARCHAR(255) NOT NULL,
    virus    VARCHAR(255) NOT NULL
);

--Relacionamento gerencia
CREATE TABLE IF NOT EXISTS gerencia (
    id_servico    INT NOT NULL references servico(id_servico),
    id_exame    INT NOT NULL references exame(id_exame)
);

--Relacionamento realiza
CREATE TABLE IF NOT EXISTS realiza (
    id_paciente    INT NOT NULL references paciente(id_paciente),
    id_exame    INT NOT NULL references exame(id_exame),
    codigo_amostra    VARCHAR(255),
    data_de_solicitacao TIMESTAMP,
    data_de_realizacao TIMESTAMP
);

--Relacionamento historico
CREATE TABLE IF NOT EXISTS historico (
    id_usuario    INT NOT NULL references paciente(id_paciente),
    id_servico    INT NOT NULL references servico(id_servico),
    id_exame    INT NOT NULL references exame(id_exame),
    data_de_utilizacao  TIMESTAMP NOT NULL
);

--Agregado amostra
CREATE TABLE IF NOT EXISTS amostra (
    id_paciente    INT NOT NULL references paciente(id_paciente),
    id_exame    INT NOT NULL references exame(id_exame),
    codigo_amostra    VARCHAR(255) NOT NULL,    
    metodo_de_coleta    VARCHAR(255) NOT NULL,
    material    VARCHAR(255) NOT NULL
);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "9761614";
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "9793714";