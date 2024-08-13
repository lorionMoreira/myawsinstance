package com.nelioalves.cursomc.projetos.services;

import org.springframework.security.core.context.SecurityContextHolder;

import com.nelioalves.cursomc.projetos.security.UserSS;
import org.springframework.security.core.Authentication;

public class UserService {

	public static UserSS authenticated() {
		try {
			return (UserSS) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
		} catch (Exception e) {
			return null;
		}
	}

	public static Authentication getLoggedInUser() {
		Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
		return authentication;

	}
}
