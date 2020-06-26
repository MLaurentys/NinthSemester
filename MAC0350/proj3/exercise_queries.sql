-- Pela forma como o pgadmin funciona, so pode ser visto o resultado da ultime query.
--  Sendo assim, para testar ou avaliar, copiar a query desejada no "scratch pad" e,
--  com esse pad selecionado, executar (F5).

-- Exercicio 4.1
SELECT
	realiza.id_exame, paciente.nome, exame.tipo,
	realiza.data_de_solicitacao, realiza.data_de_realizacao
FROM 
	realiza 
		INNER JOIN paciente
			ON realiza.id_paciente=paciente.id_paciente
		INNER JOIN exame
			ON realiza.id_exame=exame.id_exame
;

-- Exercicio 4.2
SELECT
	realiza.id_exame, 
	(realiza.data_de_realizacao - realiza.data_de_solicitacao) as atraso,
	realiza.data_de_solicitacao, realiza.data_de_realizacao
FROM
	realiza
ORDER BY 
	realiza.data_de_realizacao - realiza.data_de_solicitacao
LIMIT
	5
;

-- Exercicio 4.3
SELECT
	aux_usr.id_usuario, aux_usr.nome, aux_serv.id_servico, aux_serv.nome
FROM
	(
	SELECT 
		pertence.id_perfil, servico.id_servico, servico.nome
	 FROM
	 	pertence
	 		INNER JOIN servico
	 			ON pertence.id_servico=servico.id_servico
	) AS aux_serv
	INNER JOIN 
		(
		SELECT 
			usuario.id_usuario, usuario.nome, possui.id_perfil
		FROM
			possui
			INNER JOIN usuario
				ON possui.id_usuario=usuario.id_usuario
		) AS aux_usr
			ON aux_serv.id_perfil=aux_usr.id_perfil
ORDER BY
	aux_usr.id_usuario
;

-- Exercicio 4.4
SELECT 
	aux_usr.id_usuario, aux_usr.nome, aux_serv.id_servico,
	aux_serv.nome
FROM
	(
	SELECT
		usuario.id_usuario, usuario.nome, possui.id_perfil
	FROM
		usuario
		INNER JOIN possui
			ON usuario.id_usuario=possui.id_usuario			
	WHERE
		usuario.id_tutor IS NOT NULL
	) AS aux_usr
		INNER JOIN
			(
			SELECT 
				pertence.id_perfil, servico.id_servico, servico.nome
			 FROM
				pertence
					INNER JOIN servico
						ON pertence.id_servico=servico.id_servico
			) AS aux_serv
				ON aux_usr.id_perfil=aux_serv.id_perfil
;

-- nome (usr) | nome (perfil) | classe (serv) | count (serv)
-- Exercicio 4.5
SELECT 
	aux_serv.id_usuario, aux_serv.nome, aux_perf.id_perfil,
	aux_perf.tipo, aux_perf.id_servico, aux_serv.count
FROM
	(
	-- Todos os servicos que cada usuario realizou e quantas vezes o executou
	SELECT
		usuario.id_usuario, usuario.nome, historico.id_servico, COUNT(*)
	FROM
		historico
		INNER JOIN usuario
			ON historico.id_usuario=usuario.id_usuario
	GROUP BY
		historico.id_servico, usuario.id_usuario
	ORDER BY
		usuario.id_usuario
	) AS aux_serv
	INNER JOIN 
	(
	-- Quais servicos pertencem a cada perfil e quais usarios tem quais perfis
	SELECT
		possui.id_usuario, perfil.id_perfil, perfil.tipo, pertence.id_servico
	FROM
		perfil
		INNER JOIN pertence
			ON perfil.id_perfil=pertence.id_perfil
		INNER JOIN possui
			ON perfil.id_perfil=possui.id_perfil
	) AS aux_perf
		ON aux_serv.id_usuario=aux_perf.id_usuario
		AND aux_serv.id_servico=aux_perf.id_servico
ORDER BY
	aux_serv.count
;