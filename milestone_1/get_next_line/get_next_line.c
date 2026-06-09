/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/04 09:15:06 by amillan-          #+#    #+#             */
/*   Updated: 2025/12/09 09:57:54 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "get_next_line.h"

static char	*create_line(char *del, char *del_tmp, char *buffer)
{
	int	len;

	len = ft_strlen(del_tmp);
	del[0] = '\0';
	ft_strlcat(del, del_tmp, len + ft_strlen(buffer) + 1);
	ft_strlcat(del, buffer, len + ft_strlen(buffer) + 1);
	free(del_tmp);
	return (del);
}

static char	*fill_line(int fd, char *del, char *buffer)
{
	ssize_t	l_read;
	char	*del_tmp;

	l_read = 1;
	while (l_read > 0)
	{
		l_read = read(fd, buffer, BUFFER_SIZE);
		if (l_read == -1)
			return (NULL);
		else if (l_read == 0)
			break ;
		buffer[l_read] = '\0';
		if (!del)
			del = ft_strdup("");
		del_tmp = del;
		del = malloc(ft_strlen(del_tmp) + ft_strlen(buffer) + 1);
		if (!del)
			return (free(del_tmp), NULL);
		del = create_line(del, del_tmp, buffer);
		if (ft_strchr(buffer, '\n'))
			break ;
	}
	return (del);
}

static char	*set_new_line(char *l_buffer)
{
	char	*del;
	ssize_t	i;

	i = 0;
	while (l_buffer[i] != '\n' && l_buffer[i] != '\0')
		i++;
	if (l_buffer[0] == '\0')
		return (NULL);
	del = ft_substr(l_buffer, i + 1, ft_strlen(l_buffer) - i);
	if (del[0] == '\0')
	{
		free(del);
		del = NULL;
	}
	if (l_buffer[i] == '\n')
		l_buffer[i + 1] = '\0';
	return (del);
}

char	*get_next_line(int fd)
{
	static char	*del;
	char		*buffer;
	char		*line;

	if (fd < 0 || BUFFER_SIZE <= 0)
	{
		free(del);
		del = NULL;
		return (NULL);
	}
	buffer = malloc((BUFFER_SIZE + 1) * sizeof(char));
	if (!buffer)
		return (NULL);
	line = fill_line(fd, del, buffer);
	free(buffer);
	if (!line)
	{
		free(del);
		del = NULL;
		return (NULL);
	}
	del = set_new_line(line);
	return (line);
}
