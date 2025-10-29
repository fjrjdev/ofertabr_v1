"use client";

import Link from "next/link";
import { useState } from "react";

interface NavLinkProps {
    href: string;
    children: React.ReactNode;
    onClick?: () => void;
}

function NavLink({ href, children, onClick }: NavLinkProps) {
    return (
        <Link
            href={href}
            onClick={onClick}
            className="text-gray-700 hover:text-[#667eea] transition-colors font-medium"
        >
            {children}
        </Link>
    );
}

function MobileMenuButton({
    isOpen,
    onClick,
}: {
    isOpen: boolean;
    onClick: () => void;
}) {
    return (
        <button
            onClick={onClick}
            className="md:hidden text-gray-700 focus:outline-none"
            aria-label="Menu"
        >
            <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
            >
                {isOpen ? (
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M6 18L18 6M6 6l12 12"
                    />
                ) : (
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M4 6h16M4 12h16M4 18h16"
                    />
                )}
            </svg>
        </button>
    );
}

export function Navbar() {
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    const toggleMenu = () => setIsMenuOpen(!isMenuOpen);
    const closeMenu = () => setIsMenuOpen(false);

    return (
        <nav className="bg-white shadow-sm sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    {/* Logo */}
                    <Link
                        href="/"
                        className="text-2xl font-bold bg-gradient-to-r from-[#667eea] to-[#764ba2] bg-clip-text text-transparent"
                    >
                        OfertaBR
                    </Link>

                    {/* Desktop Navigation */}
                    <div className="hidden md:flex items-center space-x-8">
                        <NavLink href="/">Início</NavLink>
                        <NavLink href="/sobre">Sobre</NavLink>
                        <NavLink href="/planos">Planos</NavLink>
                        <NavLink href="/contato">Contato</NavLink>
                    </div>

                    {/* CTA Button - Desktop */}
                    <div className="hidden md:block">
                        <Link
                            href="/#inscrever"
                            className="bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white px-6 py-2 rounded-lg hover:shadow-lg transition-all duration-200"
                        >
                            Inscrever-se
                        </Link>
                    </div>

                    {/* Mobile Menu Button */}
                    <MobileMenuButton isOpen={isMenuOpen} onClick={toggleMenu} />
                </div>
            </div>

            {/* Mobile Menu */}
            {isMenuOpen && (
                <div className="md:hidden bg-white border-t border-gray-200">
                    <div className="px-4 pt-2 pb-4 space-y-3">
                        <div className="block">
                            <NavLink href="/" onClick={closeMenu}>
                                Início
                            </NavLink>
                        </div>
                        <div className="block">
                            <NavLink href="/sobre" onClick={closeMenu}>
                                Sobre
                            </NavLink>
                        </div>
                        <div className="block">
                            <NavLink href="/planos" onClick={closeMenu}>
                                Planos
                            </NavLink>
                        </div>
                        <div className="block">
                            <NavLink href="/contato" onClick={closeMenu}>
                                Contato
                            </NavLink>
                        </div>
                        <div className="pt-2">
                            <Link
                                href="/#inscrever"
                                onClick={closeMenu}
                                className="block w-full text-center bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white px-6 py-2 rounded-lg"
                            >
                                Inscrever-se
                            </Link>
                        </div>
                    </div>
                </div>
            )}
        </nav>
    );
}

