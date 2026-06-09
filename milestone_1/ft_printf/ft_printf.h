/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: amillan- <amillan-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/28 12:52:31 by amillan-          #+#    #+#             */
/*   Updated: 2025/12/02 09:37:37 by amillan-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H

# include <unistd.h>
# include <stdarg.h>

int	ft_printf(const char *format, ...);
int	ft_putchar(int c);
int	ft_puthex(unsigned int n, char *hex);
int	ft_putnbr(int n, int count);
int	ft_putstr(char *s);
int	ft_putunsig(unsigned int n, int count);
int	ft_putvoid(unsigned long int ptr);

#endif
