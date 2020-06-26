TRUNCATE TABLE historico, amostra, exame, gerencia, paciente, perfil,
pertence, possui, realiza, servico, tutelamento, usuario;


INSERT INTO exame
VALUES
	('1', 'PCR', 'Influenza'),
	('2', 'PCR', 'H1N1'),
	('3', 'PCR', 'COVID-19'),
	('4', 'PCR', 'SARS'),
	('5', 'Anticorpo', 'Influenza'),
	('6', 'Anticorpo', 'H1N1'),
	('7', 'Anticorpo', 'COVID-19'),
	('8', 'Anticorpo', 'SARS')
;

INSERT INTO paciente
VALUES
	('1', '23124312218', 'Juliano', 'Farialimer', '1997/11/10'),
	('2', '77678784547', 'Guilherme', 'Osasco', '1998/08/12'),
	('3', '53425456248', 'Sofia', 'Interlagos', '1998/07/14'),
	('4', '12352436276', 'Victor', 'Mooca', '1997/10/24')
;

INSERT INTO amostra
VALUES
	('1', '2', '1', 'vias aereas', 'catarro'),
	('2', '1', '2', 'vias aereas', 'saliva')
;

INSERT INTO realiza
VALUES
	('1', '2', '1', '2020/05/25', '2020/05/30'),
	('1', '6', '2', '2020/05/25', '2020/06/01'),
	('2', '1', '3', '2020/05/10', '2020/05/27'),
	('2', '5', '4', '2020/05/10', '2020/06/10'),
	('3', '3', '5', '2020/03/05', '2020/03/06'),
	('3', '7', '6', '2020/03/05', '2020/03/07'),
	('4', '4', '7', '2020/04/01', '2020/04/30'),
	('4', '8', '8', '2020/04/01', '2020/05/01')
;

INSERT INTO perfil
VALUES
	('1', '1', 'administrador do BD'),
	('2', '2', 'pesquisador'),
	('3', '3', 'Super Admin do BD')
;

INSERT INTO servico
VALUES
	('1', 'ver resultado PCR', 'visualização'),
	('2', 'ver resultado Anticorpo', 'visualização'),
	('3', 'remover', 'remoção'),
	('4', 'inserir', 'inserção'),
	('5', 'modificar', 'alteração'),
	('6', 'alterar informacoes', 'alteração')
;

INSERT INTO pertence
VALUES
	('1', '2'),
	('2', '2'),
	('4', '2'),
	('5', '2'),
	('1', '1'),
	('2', '1'),
	('3', '1'),
	('4', '1'),
	('5', '1'),
	('1', '3'),
	('2', '3'),
	('3', '3'),
	('4', '3'),
	('5', '3'),
	('6', '3')
;

INSERT INTO gerencia
VALUES
	('2', '1'),
	('1', '2'),
	('3', '1'),
	('4', '1'),
	('5', '1'),
	('3', '2'),
	('4', '2'),
	('5', '2')	
;

INSERT INTO usuario
VALUES
	('1', '64980792405', 'Matheus', 'computacao', 'IME', '1998/03/21', 'mtl', 'teste1', NULL),
	('2', '17767587304', 'Allan', 'biologia', 'IB', '1998/05/10', 'aln', 'teste2', NULL),
	('3', '17767542352', 'Joao', 'historia', 'FFLCH', '1990/09/03', 'jef', 'teste3', NULL),
	('4', '43242523422', 'Padilha', 'comunicacao', 'ECA', '1996/12/01', 'pdl', 'teste4', '3')
;

INSERT INTO tutelamento
VALUES
	('4', '2', '1', '2', '2020/02/01', '2020/07/01'),
	('4', '2', '2', '2', '2020/02/01', '2020/07/01'),
	('4', '2', '4', '2', '2020/02/01', '2020/07/01'),
	('4', '2', '5', '2', '2020/02/01', '2020/07/01')

;

INSERT INTO possui
VALUES
	('1', '1'),
	('3', '1'),
	('3', '3'),
	('2', '2'),
	('4', '2')
;

-- Matheus e JEF inserem os exames, depois Allan e Padilha consultam.
INSERT INTO historico
VALUES
	('1', '4', '1', '2020/06/11'),
	('1', '4', '3', '2020/06/12'),
	('1', '4', '5', '2020/06/13'),
	('1', '2', '3', '2020/06/13'),
	('2', '1', '1', '2020/06/16'),
	('2', '1', '2', '2020/06/17'),
	('2', '2', '6', '2020/06/18'),
	('3', '4', '7', '2020/06/14'),
	('3', '4', '2', '2020/06/11'),
	('3', '4', '4', '2020/06/12'),
	('3', '4', '6', '2020/06/13'),
	('3', '4', '8', '2020/06/13'),
	('3', '6', '8', '2020/06/20'),
	('4', '1', '2', '2020/06/17'),
	('4', '2', '8', '2020/06/19'),
	('4', '5', '8', '2020/06/21'),
	('4', '2', '8', '2020/06/20')
;




